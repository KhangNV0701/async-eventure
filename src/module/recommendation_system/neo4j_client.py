from collections import defaultdict

import pandas as pd
from neo4j import GraphDatabase


class Neo4jClient:
    def __init__(self, url, username, password):
        self.driver = GraphDatabase.driver(url, auth=(username, password))

    def process_query(self, query, params={}):
        with self.driver.session() as session:
            result = session.run(query=query, parameters=params)
            return pd.DataFrame(
                data=[r.values() for r in result], columns=result.keys()
            )

    def upsert_event(self, event):
        """
        Insert/Update event to neo4j graph database.

        Args:
            event (dict)
            - id (str)
            - categories (str)
            - name (str)
            - tags (list of str)
        """
        queries = [
            """
            MERGE (e: Event {id: $event.id})
            ON CREATE SET
                e.id = $event.id,
                e.name = $event.name,
                e.tags = $event.tags
            ON MATCH SET e.name = $event.name, e.tags = $event.tags
            """,
            """
            MATCH (e: Event {id: $event.id}) - [r:IN_CATEGORY] -> (c: Category)
            DELETE r
            """,
            """
            UNWIND $event.categories as category_id
            MATCH (e:Event {id: $event.id}), (c:Category {id: category_id})
            WHERE NOT EXISTS((e)-[:IN_CATEGORY]->(c))
            CREATE (e)-[:IN_CATEGORY]->(c)
            """
        ]
        for query in queries:
            self.process_query(query=query, params={'event': event})

    def delete_event(self, event_id):
        """
        Delete an event in neo4j graph database.

        Args:
            event_id (str)
        """
        query = """
            MATCH (e:Event {id: $event_id})
            DETACH DELETE e
            """
        self.process_query(query=query, params={'event_id': event_id})

    def upsert_user(self, user):
        """
        Insert/Update user to neo4j graph database
        Args:
            user (dict)
            - id (str)
            - categories (list of str)
        """

        queries = [
            """
            MERGE (u: User {id: $user_id})
            ON CREATE SET u.id = $user_id
            """,
            """
            MATCH (e: User {id: $user_id}) - [r:PREFERRED] -> (c: Category)
            DELETE r
            """
        ]
        for query in queries:
            self.process_query(query=query, params={'user_id': user['id']})

        query = """
            MATCH (u:User {id: $user_id}), (c:Category {id: $category_id})
            WHERE NOT EXISTS((u)-[:PREFERRED]->(c))
            CREATE (u)-[:PREFERRED]->(c)
            """
        for category_id in user['categories']:
            self.process_query(
                query=query,
                params={
                    'user_id': user['id'],
                    'category_id': category_id
                }
            )

    def delete_user(self, user_id):
        """
        Delete user in neo4j graph database
        Args: user_id (str)
        """
        query = """
            MATCH (u:User {id: $user_id})
            DETACH DELETE u
            """
        self.process_query(query=query, params={'user_id': user_id})

    def view_event(self, user_id, event_id):
        """
        Add VIEWED edge between user and event in neo4j graph database
        when user follows an event.

        Args:
            user_id (str),
            event_id (str)
        """
        query = """
            MATCH (u:User {id: $user_id}), (e:Event {id: $event_id})
            WHERE NOT EXISTS((u)-[:VIEWED]->(e))
            CREATE (u)-[:VIEWED]->(e)
            """
        self.process_query(query=query, params={'user_id': user_id, 'event_id': event_id})

    def like_event(self, user_id, event_id):
        """
        Add LIKED edge between user and event in neo4j graph database
        when user likes an event

        Args:
            user_id (str)
            event_id (str)
        """
        query = """
            MATCH (u:User {id: $user_id}), (e:Event {id: $event_id})
            WHERE NOT EXISTS((u)-[:LIKED]->(e))
            CREATE (u)-[:LIKED]->(e)
            """
        self.process_query(
            query=query,
            params={'user_id': user_id, 'event_id': event_id}
        )

    def unfollow_event(self, user_id, event_id):
        """
        Remove LIKED edge between user and event in neo4j graph database
        when user likes an event

        Args:
            user_id (str)
            event_id (str)
        """
        query = """
            MATCH (u:User {id: $user_id}) - [r:LIKED] -> (e:Event {id: $event_id})
            DELETE r
            """
        self.process_query(
            query=query,
            params={'user_id': user_id, 'event_id': event_id}
        )

    def get_user_most_view_category(self, user_id):
        """
        Get user most view category based on view/follow actions.
        Limit to 3 most categories
        Args: user_id (str)
        """
        query = """
            MATCH (u:User {id: $user_id}) - [:VIEWED|FOLLOWED] - (e:Event) - [:IN_CATEGORY] -> (c:Category)
            WITH c.name AS category_name, count(c.id) AS event_count, c.id as category_id
            ORDER BY event_count DESC
            LIMIT 3
            RETURN category_id, category_name, event_count;
            """
        with self.driver.session() as session:
            k_most_categories = session.run(
                query=query,
                user_id=user_id
            ).values()

        return k_most_categories

    def get_user_preferences(self, user_id):
        """
        Get user's favorite categories
        Args: user_id (str)
        """
        query = """
            MATCH (u:User {id:$user_id}) - [] -> (c:Category)
            return c.id, c.name
        """
        with self.driver.session() as session:
            fav_categories = session.run(
                query=query,
                user_id=user_id
            ).values()
        return fav_categories

    def get_recommendation(self, user_id, k = 20):
        """
        Recommend 20 events for user based on most view category & preferences.
        Args: user_id (str)
        """
        query = """
            MATCH (p1:User {id: $user_id})
            MATCH (p2:User) WHERE p1 <> p2
            WITH gds.alpha.linkprediction.adamicAdar(p1, p2) AS aA, p2.id as ids
            ORDER BY aA DESC
            LIMIT 10
            UNWIND ids as id 
            MATCH (a:User {id:id})-[r:VIEWED|LIKED]->(e:Event) 
            WITH e, id LIMIT $k
            WITH e, e.id as event_id, e.name as event_name
            WITH e {event_id, event_name} as entry
            RETURN collect(entry) as info
        """
        res = []
        neo4j_response = self.process_query(query, params = {'user_id': user_id, 'k': k})
        for index, row in neo4j_response.iterrows():
            for ele in row['info']:
                res.append(ele['event_id'])
        return res
