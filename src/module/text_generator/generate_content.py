import json

from tenacity import retry, stop_after_attempt, stop_after_delay, wait_fixed

from src.config.constant import geminiAiCFG
from src.module.gemini.gemini_client import GeminiAI
from src.module.gemini.prompts import (PROMPT_GENERATE_EVENT_CONTENT,
                                       PROMPT_GENERATE_EVENT_FAQ)
from src.utils.logger import logger


@retry(stop=(stop_after_delay(30) | stop_after_attempt(3)), wait=wait_fixed(1))
def call_model_gen_content(prompt):
    logger.info("GENERATE EVENT CONTENT PROMPT:\n%s", prompt)
    gemini_client = GeminiAI(
        API_KEY=geminiAiCFG.API_KEY,
        API_MODEL=geminiAiCFG.API_MODEL
    )
    generated_content = gemini_client.generate_content_json(prompt)
    return generated_content


def generate_event_content(event_data):
    formatted_prompt = PROMPT_GENERATE_EVENT_CONTENT.format(
        event_name=event_data.event_name,
        event_format=event_data.event_format,
        event_categories=event_data.event_categories,
        event_description=event_data.event_description,
        event_detail_info=event_data.event_detail_info
    )

    generated_content = call_model_gen_content(formatted_prompt)
    generated_content = process_event_content(generated_content)

    logger.info(
        "GENERATED EVENT CONTENT: %s", str(json.dumps(
            generated_content, indent=4, ensure_ascii=True))
    )
    return generated_content


def generate_event_faq(event_data):
    formatted_prompt = PROMPT_GENERATE_EVENT_FAQ.format(
        event_name=event_data.event_name,
        event_format=event_data.event_format,
        event_categories=event_data.event_categories,
        event_description=event_data.event_description,
        event_detail_info=event_data.event_detail_info
    )

    generated_faq = call_model_gen_content(formatted_prompt)
    generated_faq = {"faqs": generated_faq}

    logger.info(
        "GENERATED EVENT FAQ: %s", str(json.dumps(
            generated_faq, indent=4, ensure_ascii=True))
    )
    return generated_faq


def process_event_content(event_content):
    tags = event_content.get("tags", [])
    event_content["tags"] = [
        "-".join(str(tag).lower().split(" ")) for tag in tags
    ]

    return event_content
