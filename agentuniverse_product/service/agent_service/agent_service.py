# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Time    : 2024/7/25 21:11
# @Author  : wangchongshi
# @Email   : wangchongshi.wcs@antgroup.com
# @FileName: agent_service.py
from typing import List

from agentuniverse.agent.agent import Agent
from agentuniverse.agent.agent_model import AgentModel
from agentuniverse.base.component.component_enum import ComponentEnum
from agentuniverse.llm.llm import LLM
from agentuniverse.llm.llm_manager import LLMManager
from agentuniverse.prompt.prompt import Prompt
from agentuniverse.prompt.prompt_manager import PromptManager
from agentuniverse.prompt.prompt_model import AgentPromptModel
from agentuniverse_product.base.product import Product
from agentuniverse_product.base.product_manager import ProductManager
from agentuniverse_product.service.model.agent_dto import AgentDTO
from agentuniverse_product.service.model.llm_dto import LlmDTO
from agentuniverse_product.service.model.prompt_dto import PromptDTO


class AgentService:

    @staticmethod
    def get_agent_list() -> List[AgentDTO]:
        res = []
        product_list: List[Product] = ProductManager().get_instance_obj_list()
        if len(product_list) < 1:
            return res
        for product in product_list:
            if product.type == ComponentEnum.AGENT.value:
                agent_dto = AgentDTO(nickname=product.nickname, avatar=product.avatar, id=product.id)
                agent = product.instance
                agent_model: AgentModel = agent.agent_model
                agent_dto.description = agent_model.info.get('description', '')
                res.append(agent_dto)
        return res

    @staticmethod
    def get_agent_detail(id: str) -> AgentDTO | None:
        product_list: List[Product] = ProductManager().get_instance_obj_list()
        if len(product_list) < 1:
            return None
        for product in product_list:
            if product.type == ComponentEnum.AGENT.value and product.id == id:
                agent_dto = AgentDTO(nickname=product.nickname, avatar=product.avatar, id=product.id,
                                     opening_speech=product.opening_speech)
                agent: Agent = product.instance
                agent_model: AgentModel = agent.agent_model
                agent_dto.description = agent_model.info.get('description', '')
                agent_dto.prompt = AgentService.get_prompt_dto(agent_model)
                agent_dto.llm = AgentService.get_llm_dto(agent_model)
                agent_dto.memory = agent_model.memory.get('name', '')
                return agent_dto
        return None

    @staticmethod
    def get_prompt_dto(agent_model: AgentModel) -> PromptDTO:
        profile_prompt_model: AgentPromptModel = AgentPromptModel(
            introduction=agent_model.profile.get('introduction'),
            target=agent_model.profile.get('target'),
            instruction=agent_model.profile.get('instruction'))

        prompt_version = agent_model.profile.get('prompt_version')
        version_prompt: Prompt = PromptManager().get_instance_obj(prompt_version)

        if version_prompt is None and not profile_prompt_model:
            raise Exception("Either the `prompt_version` or `introduction & target & instruction`"
                            " in agent profile configuration should be provided.")
        if version_prompt:
            version_prompt_model: AgentPromptModel = AgentPromptModel(
                introduction=getattr(version_prompt, 'introduction', ''),
                target=getattr(version_prompt, 'target', ''),
                instruction=getattr(version_prompt, 'instruction', ''))
            profile_prompt_model = profile_prompt_model + version_prompt_model

        return PromptDTO(introdcution=profile_prompt_model.introduction, target=profile_prompt_model.target,
                         instruction=profile_prompt_model.instruction)

    @staticmethod
    def get_llm_dto(agent_model: AgentModel) -> LlmDTO | None:
        llm_model = agent_model.profile.get('llm_model', {})
        llm_id = llm_model.get('name')
        llm: LLM = LLMManager().get_instance_obj(llm_id)
        product: Product = ProductManager().get_instance_obj(llm_id)
        if llm is None or product is None:
            return None
        return LlmDTO(id=llm_id, nickname=product.nickname, temperature=llm.temperature)