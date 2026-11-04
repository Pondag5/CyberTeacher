# Prompt Engine Builder

import json
import os
from typing import Optional, Dict, Any, List

class PromptBuilder:
    """
    Comprehensive prompt builder for CyberTeacher's AI teacher.
    Handles all prompt modifiers and context components.
    """
    
    def __init__(self, mode: str, context_str: str = "", docs_context: str = "", study_context: str = ""):
        self.mode = mode
        self.context_str = context_str
        self.docs_context = docs_context
        self.study_context = study_context
        self.system_prompt = ""
        self.modifiers = []
        
        # Load base prompt from config
        self._load_base_prompt()
        
    def _load_base_prompt(self):
        """Load the base system prompt from teacher_prompts.json"""
        prompts_path = os.path.join("config", "teacher_prompts.json")
        try:
            with open(prompts_path, "r", encoding="utf-8") as f:
                prompts_data = json.load(f)
            base_prompt = prompts_data.get("system_prompt", 
                "РўС‹ - СѓС‡РёС‚РµР»СЊ РєРёР±РµСЂР±РµР·РѕРїР°СЃРЅРѕСЃС‚Рё.")
            
            personas = prompts_data.get("personas", {})
            persona = self._get_current_persona()
            persona_instructions = personas.get(persona, {}).get("instructions", [])
            
            if persona_instructions:
                base_prompt += "\n\nРРЅСЃС‚СЂСѓРєС†РёРё РґР»СЏ СЂРµР¶РёРјР°:\n" + "\n".join(
                    [f"- {p}" for p in persona_instructions]
                )
            
            self.system_prompt = base_prompt
        except (OSError, IOError, json.JSONDecodeError):
            self.system_prompt = "РўС‹ - СѓС‡РёС‚РµР»СЊ РєРёР±РµСЂР±РµР·РѕРїР°СЃРЅРѕСЃС‚Рё."
    
    def _get_current_persona(self) -> str:
        """Get current persona from state"""
        try:
            from src.core.state import get_state
            state = get_state()
            return state.get_persona()
        except ImportError:
            return "default"
    
    def add_study_context(self, study_context: str):
        """Add study context to prompt"""
        self.study_context = study_context
        if study_context:
            self.system_prompt += f"\n\nРљРћРќРўР•РљРЎРў РЈР§Р•РќРРљРђ:\n{study_context}"
    
    def add_docs_context(self, docs_context: str):
        """Add RAG context from knowledge base"""
        self.docs_context = docs_context
        if docs_context:
            self.system_prompt += f"\n\nР”РђРќРќР«Р• РР— Р‘РђР—Р« Р—РќРђРќРР™:\n{docs_context}"
    
    def add_modifier(self, modifier: str):
        """Add a modifier to the prompt"""
        if modifier:
            self.modifiers.append(modifier)
        return self
    
    def build(self) -> str:
        """Build the complete system prompt"""
        prompt = self.system_prompt
        
        # Add study context if provided
        if self.study_context:
            prompt += f"\n\nРљРћРќРўР•РљРЎРў РЈР§Р•РќРРљРђ:\n{self.study_context}"
        
        # Add docs context if provided
        if self.docs_context:
            prompt += f"\n\nР”РђРќРќР«Р• РР— Р‘РђР—Р« Р—РќРђРќРР™:\n{self.docs_context}"
        
        # Add all modifiers
        for modifier in self.modifiers:
            prompt += f"\n\n{modifier}"
        
        return prompt
    
    def get_modifiers(self) -> List[str]:
        """Return all added modifiers"""
        return self.modifiers
    
    def get_context(self) -> Dict[str, str]:
        """Return context components"""
        return {
            "study_context": self.study_context,
            "docs_context": self.docs_context
        }


class PromptContext:
    """
    Context manager for prompt building with various modifiers.
    """
    
    def __init__(self, mode: str):
        self.builder = PromptBuilder(mode)
    
    def add_modifier(self, modifier: str) -> "PromptContext":
        """Add a modifier to the prompt"""
        self.builder.add_modifier(modifier)
        return self
    
    def with_study_context(self, context: str) -> "PromptContext":
        """Add study context to the prompt"""
        self.builder.add_study_context(context)
        return self
    
    def with_docs_context(self, context: str) -> "PromptContext":
        """Add RAG context from knowledge base"""
        self.builder.add_docs_context(context)
        return self
    
    def with_atmosphere(self, atmosphere: str) -> "PromptContext":
        """Add atmosphere modifier"""
        self.builder.add_modifier(atmosphere)
        return self
    
    def with_personality_drift(self, drift: str) -> "PromptContext":
        """Add personality drift modifier"""
        self.builder.add_modifier(drift)
        return self
    
    def with_archetype(self, archetype: str) -> "PromptContext":
        """Add behavioral archetype modifier"""
        self.builder.add_modifier(archetype)
        return self
    
    def with_persona(self, persona: str) -> "PromptContext":
        """Add persona router modifier"""
        self.builder.add_modifier(persona)
        return self
    
    def with_cyberpsychosis(self, cp: str) -> "PromptContext":
        """Add cyberpsychosis modifier"""
        self.builder.add_modifier(cp)
        return self
    
    def with_difficulty(self, difficulty: str) -> "PromptContext":
        """Add adaptive difficulty modifier"""
        self.builder.add_modifier(difficulty)
        return self
    
    def build(self) -> str:
        """Build the complete system prompt"""
        return self.builder.build()


# Example usage:
# context = PromptContext("chat")
# context.with_study_context(study_context).with_docs_context(docs_context).with_atmosphere(atmosphere).build()