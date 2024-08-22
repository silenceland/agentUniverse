# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# @Time    : 2024/8/5 14:37
# @Author  : fanen.lhy
# @Email   : fanen.lhy@antgroup.com
# @FileName: text_splitter.py
from typing import List, Optional
from langchain.text_splitter import CharacterTextSplitter as Splitter

from agentuniverse.agent.action.knowledge.doc_processor.doc_processor import \
    DocProcessor
from agentuniverse.agent.action.knowledge.store.document import Document
from agentuniverse.agent.action.knowledge.store.query import Query
from agentuniverse.base.config.component_configer.component_configer import \
    ComponentConfiger


class CharacterTextSplitter(DocProcessor):
    chunk_size: int = 200
    chunk_overlap: int = 20
    separator: str = "/n/n"
    splitter: Optional[Splitter] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.splitter = Splitter(separator=self.separator,
                                 chunk_size=self.chunk_size,
                                 chunk_overlap=self.chunk_overlap)

    def _process_docs(self, origin_docs: List[Document], query: Query = None) -> \
            List[Document]:
        lc_doc_list = self.splitter.split_documents(Document.as_langchain_list(
            origin_docs
        ))
        return Document.from_langchain_list(lc_doc_list)

    def _initialize_by_component_configer(self,
                                         doc_processor_configer: ComponentConfiger) -> 'DocProcessor':
        super()._initialize_by_component_configer(doc_processor_configer)
        if hasattr(doc_processor_configer, "chunk_size"):
            self.chunk_size = doc_processor_configer.chunk_size
        if hasattr(doc_processor_configer, "chunk_overlap"):
            self.chunk_overlap = doc_processor_configer.chunk_overlap
        if hasattr(doc_processor_configer, "separator"):
            self.separator = doc_processor_configer.separator
        self.splitter = Splitter(separator=self.separator,
                                 chunk_size=self.chunk_size,
                                 chunk_overlap=self.chunk_overlap)
        return self