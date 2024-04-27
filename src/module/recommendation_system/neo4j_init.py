from collections import defaultdict
import pandas as pd
from neo4j import GraphDatabase
import mysql.connector
from src.utils.logger import logger

class Neo4jInit:
    def __init__(self, url, username, password):
        self.driver = GraphDatabase.driver(url, auth=(username, password))
        self.connection = mysql.connector.connect(
            host="localhost",
            user="myuser",
            password="mypassword",
            database="eventure"
            )
    
    def init_neo4j(self):
        self.clear_all()
        self.create_constraint()
        self.add_user()
        self.add_event()
        self.add_category()
        self.add_ec_edge()
        self.add_uc_edge()
        self.add_view_edge()
    
    def clear_all(self):
        query = """
        MATCH (n)
        DETACH DELETE n;
        """
        with self.driver.session() as session:
            session.run(query)
        logger.info("CLEARED NEO4J")
    
    def create_constraint(self):
        queries = ['CREATE CONSTRAINT users IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE',
                'CREATE CONSTRAINT events IF NOT EXISTS FOR (e:Event) REQUIRE e.id IS UNIQUE',
                'CREATE CONSTRAINT categories IF NOT EXISTS FOR (c:Category) REQUIRE c.id IS UNIQUE']
        for query in queries:
            with self.driver.session() as session:
                session.run(query)
        logger.info("CREATED CONSTRAINTS")
    
    def add_user(self):
        query = "select * from user_account"
        user_ids = []

        with self.connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            for row in result:
                user_ids.append(row[0])

        query = """
        UNWIND $ids AS id
        MERGE (u: User {id: id})
        ON CREATE SET u.id = id
        """

        with self.driver.session() as session:
            session.run(query, ids=user_ids)

        query = """
        MATCH (n:User)
        return n
        """

        with self.driver.session() as session:
            result = session.run(query).values()

        logger.info("Users mysql: " + str(len(user_ids)) + "    Users neo4j: " + str(len(result)))
        logger.info("ADDED USER")
    
    def add_event(self):
        query = "select * from event"
        event_ids = []

        with self.connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            for row in result:
                event_ids.append(row[0])

        query = """
        UNWIND $ids AS id
        MERGE (e: Event {id: id})
        ON CREATE SET e.id = id
        """

        with self.driver.session() as session:
            session.run(query, ids=event_ids)

        query = """
        MATCH (n:Event)
        return n
        """

        with self.driver.session() as session:
            result = session.run(query).values()

        logger.info("Events mysql: " + str(len(event_ids)) + "    Events neo4j: " + str(len(result)))
        logger.info("ADDED EVENT")
    
    def add_category(self):
        query = "select * from category"
        category_ids = []

        with self.connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            for row in result:
                category_ids.append(row[0])

        query = """
        UNWIND $ids AS id
        MERGE (c: Category {id: id})
        ON CREATE SET c.id = id
        """

        with self.driver.session() as session:
            session.run(query, ids=category_ids)

        query = """
        MATCH (n:Category)
        return n
        """

        with self.driver.session() as session:
            result = session.run(query).values()

        logger.info("Events mysql: " + str(len(category_ids)) + "    Events neo4j: " + str(len(result)))
        logger.info("ADDED CATEGORY")
    
    def add_ec_edge(self):
        query = "select event_id, category_id from event_category"

        event_category_edges = []

        with self.connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            for row in result:
                event_category_edges.append({'from': row[0], 'to': row[1]})

        query = """
        UNWIND $edges as edge
        MATCH (e:Event {id: edge.from}), (c:Category {id: edge.to})
        WHERE NOT EXISTS((e)-[:IN_CATEGORY]->(c))
        CREATE (e)-[:IN_CATEGORY]->(c)
        """

        with self.driver.session() as session:
            session.run(query, edges=event_category_edges)

        query = """
        MATCH (e:Event) - [r] -> (c:Category)
        return count(r)
        """

        with self.driver.session() as session:
            result = session.run(query).values()

        logger.info("EC edges mysql: " + str(len(event_category_edges)) + "    EC edges neo4j: " + str(len(result)))
        logger.info("ADDED EC EDGE")

    def add_uc_edge(self):
        query = "select username, category_id from user_interests"

        user_category_edges = []

        with self.connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            for row in result:
                user_category_edges.append({'from': row[0], 'to': row[1]})

        query = """
        UNWIND $edges as edge
        MATCH (u:User {id: edge.from}), (c:Category {id: edge.to})
        WHERE NOT EXISTS((u)-[:PREFERRED]->(c))
        CREATE (u)-[:PREFERRED]->(c)
        """

        with self.driver.session() as session:
            session.run(query, edges=user_category_edges)

        query = """
        MATCH (u:User) - [r] -> (c:Category)
        return count(r)
        """

        with self.driver.session() as session:
            result = session.run(query).values()

        logger.info("UC edges mysql: " + str(len(user_category_edges)) + "    UC edges neo4j: " + str(len(result)))
        logger.info("ADDED UC EDGE")
    
    def add_view_edge(self):
        query = """
        MATCH (u:User) - [r1:PREFERRED] -> (c:Category) <- [r2:IN_CATEGORY] - (e:Event)
        WHERE NOT EXISTS((u)-[:VIEWED]->(e))
        CREATE (u)-[ed:VIEWED]->(e)
        """

        with self.driver.session() as session:
            result = session.run(query)
        
        logger.info("ADDED VIEWED EDGE")