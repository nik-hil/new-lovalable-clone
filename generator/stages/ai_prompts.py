#!/usr/bin/env python3
"""
AI Prompts for Multi-Stage Store Website Generation

Contains structured prompts for each stage of the generation pipeline:
1. Design Brief Generation
2. Architecture Planning  
3. Component Generation
4. Integration & Assembly
5. Validation & Refinement
"""

from typing import Dict, Any, List
from dataclasses import dataclass
import json

@dataclass
class PromptTemplate:
    """Template for AI prompts with context and formatting"""
    system_prompt: str
    user_prompt_template: str
    output_schema: Dict[str, Any]
    temperature: float = 0.7
    max_tokens: int = 4000

class AIPrompts:
    """Collection of AI prompts for store generation"""
    
    @staticmethod
    def get_design_brief_prompt() -> PromptTemplate:
        """Generate design brief from user input"""
        
        system_prompt = """You are an expert UX/UI designer specializing in modern e-commerce websites for small local businesses. You create comprehensive design briefs that capture brand personality, target audience, and design requirements.

Your expertise includes:
- Modern web design trends and best practices
- E-commerce UX patterns and conversion optimization
- Brand identity and visual design systems
- Accessibility and responsive design principles
- Small business needs and constraints

Always create designs that are:
- Professional yet approachable
- Modern and trustworthy
- Optimized for conversions
- Accessible and user-friendly
- Suitable for the target demographic"""

        user_prompt_template = """Create a comprehensive design brief for: {user_prompt}

Consider the business type, target audience, and create a detailed design strategy.

Analysis Context:
- This is for a local mom-and-pop store website
- Must include e-commerce functionality (shopping cart, checkout)
- Should feel modern but approachable
- Target audience is local community members
- Budget-conscious but quality-focused

Please analyze the request and create a detailed design brief."""

        output_schema = {
            "business_analysis": {
                "business_type": "string",
                "store_category": "string (flower_shop, coffee_shop, bakery, retail, restaurant, bookstore)",
                "target_audience": "string",
                "unique_selling_points": ["string"],
                "competitive_advantages": ["string"]
            },
            "brand_identity": {
                "brand_personality": ["string"],
                "brand_values": ["string"],
                "tone_of_voice": "string",
                "visual_style": "string"
            },
            "design_direction": {
                "color_palette": {
                    "primary": "string (hex color)",
                    "secondary": "string (hex color)", 
                    "accent": "string (hex color)",
                    "description": "string"
                },
                "typography": {
                    "primary_font": "string",
                    "secondary_font": "string",
                    "style_description": "string"
                },
                "imagery_style": "string",
                "layout_approach": "string"
            },
            "user_experience": {
                "key_user_journeys": ["string"],
                "priority_features": ["string"],
                "conversion_goals": ["string"]
            },
            "technical_requirements": {
                "pages_needed": ["string"],
                "components_needed": ["string"],
                "integrations_required": ["string"]
            }
        }
        
        return PromptTemplate(
            system_prompt=system_prompt,
            user_prompt_template=user_prompt_template,
            output_schema=output_schema,
            temperature=0.8,
            max_tokens=3000
        )
    
    @staticmethod
    def get_architecture_prompt() -> PromptTemplate:
        """Generate technical architecture from design brief"""
        
        system_prompt = """You are a senior full-stack architect specializing in modern Vue.js e-commerce applications. You design scalable, maintainable architectures for small business websites.

Your expertise includes:
- Vue.js 3 with Composition API and TypeScript
- Modern state management with Pinia
- Component-driven architecture and design systems
- RESTful API design and database modeling
- Performance optimization and SEO best practices

You always create architectures that are:
- Scalable and maintainable
- Following modern Vue.js best practices  
- Optimized for performance and SEO
- Accessible and responsive
- Easy for small businesses to manage"""

        user_prompt_template = """Based on this design brief, create a technical architecture plan:

{design_brief}

Design System Tokens Available:
{design_tokens}

Template Components Available:
{available_components}

Create a comprehensive technical architecture that uses our existing design system and components."""

        output_schema = {
            "site_structure": {
                "pages": [
                    {
                        "name": "string",
                        "path": "string",
                        "purpose": "string",
                        "components_needed": ["string"]
                    }
                ],
                "navigation_structure": {
                    "main_nav": ["string"],
                    "footer_nav": ["string"],
                    "user_nav": ["string"]
                }
            },
            "component_plan": {
                "layout_components": ["string"],
                "ui_components": ["string"], 
                "business_components": ["string"],
                "custom_components_needed": [
                    {
                        "name": "string",
                        "purpose": "string",
                        "props": ["string"],
                        "functionality": "string"
                    }
                ]
            },
            "data_architecture": {
                "entities": [
                    {
                        "name": "string",
                        "fields": ["string"],
                        "relationships": ["string"]
                    }
                ],
                "api_endpoints": [
                    {
                        "path": "string",
                        "method": "string",
                        "purpose": "string"
                    }
                ]
            },
            "state_management": {
                "stores_needed": [
                    {
                        "name": "string",
                        "purpose": "string",
                        "state_fields": ["string"],
                        "actions": ["string"]
                    }
                ],
                "data_flow": "string"
            },
            "styling_approach": {
                "design_tokens_usage": "string",
                "custom_styles_needed": ["string"],
                "responsive_strategy": "string"
            }
        }
        
        return PromptTemplate(
            system_prompt=system_prompt,
            user_prompt_template=user_prompt_template,
            output_schema=output_schema,
            temperature=0.6,
            max_tokens=3500
        )
    
    @staticmethod
    def get_component_generation_prompt() -> PromptTemplate:
        """Generate Vue.js components from architecture"""
        
        system_prompt = """You are an expert Vue.js developer specializing in modern e-commerce components. You write clean, maintainable Vue.js 3 code using Composition API and TypeScript.

Your code always follows these principles:
- Vue.js 3 Composition API with `<script setup lang="ts">`
- Proper TypeScript interfaces for props and emits
- Tailwind CSS for styling with design system tokens
- Accessible HTML with proper ARIA labels
- Responsive design with mobile-first approach
- Clean, readable code with proper error handling

You integrate seamlessly with existing components and design systems."""

        user_prompt_template = """Generate a Vue.js component based on this specification:

Component Specification:
{component_spec}

Architecture Context:
{architecture_plan}

Design System Tokens:
{design_tokens}

Existing Components to Reference:
{reference_components}

Requirements:
- Use Vue.js 3 Composition API with TypeScript
- Follow our design system tokens and patterns
- Ensure accessibility and responsive design
- Include proper error handling and loading states
- Match the style and patterns of existing components"""

        output_schema = {
            "component": {
                "name": "string",
                "file_path": "string",
                "template": "string",
                "script": "string", 
                "style": "string",
                "props_interface": "string",
                "emits_interface": "string"
            },
            "dependencies": ["string"],
            "usage_example": "string",
            "testing_considerations": ["string"]
        }
        
        return PromptTemplate(
            system_prompt=system_prompt,
            user_prompt_template=user_prompt_template,
            output_schema=output_schema,
            temperature=0.4,
            max_tokens=4000
        )
    
    @staticmethod
    def get_integration_prompt() -> PromptTemplate:
        """Generate integration code and configuration"""
        
        system_prompt = """You are a senior full-stack developer who specializes in integrating Vue.js frontends with Flask backends and ensuring all components work together seamlessly.

Your expertise includes:
- Vue.js application configuration and routing
- Pinia store integration and data flow
- API integration with error handling
- Build configuration and deployment
- Performance optimization

You always ensure:
- Proper error handling and user feedback
- Optimal loading states and UX
- SEO-friendly configuration
- Production-ready code quality"""

        user_prompt_template = """Create integration code for this store website:

Architecture Plan:
{architecture_plan}

Generated Components:
{generated_components}

API Endpoints:
{api_endpoints}

Requirements:
- Set up Vue Router with all pages
- Configure Pinia stores with API integration  
- Create main App.vue and main.ts
- Set up proper error handling
- Ensure responsive layout and navigation"""

        output_schema = {
            "app_files": {
                "main_ts": "string",
                "app_vue": "string", 
                "router_config": "string"
            },
            "store_configurations": [
                {
                    "store_name": "string",
                    "file_content": "string"
                }
            ],
            "config_files": {
                "package_json": "string",
                "tsconfig_json": "string",
                "vite_config": "string",
                "tailwind_config": "string"
            },
            "api_integration": {
                "axios_config": "string",
                "error_handling": "string"
            }
        }
        
        return PromptTemplate(
            system_prompt=system_prompt,
            user_prompt_template=user_prompt_template,
            output_schema=output_schema,
            temperature=0.3,
            max_tokens=4000
        )
    
    @staticmethod
    def get_validation_prompt() -> PromptTemplate:
        """Validate and refine generated code"""
        
        system_prompt = """You are a senior code reviewer and quality assurance expert specializing in Vue.js e-commerce applications.

You analyze code for:
- Vue.js best practices and patterns
- TypeScript type safety
- Accessibility compliance (WCAG)
- Performance optimization
- Security considerations
- Code maintainability and readability

You provide specific, actionable feedback and corrections."""

        user_prompt_template = """Review and validate this generated store website:

Generated Code:
{generated_code}

Validation Report:
{validation_report}

Design Requirements:
{design_brief}

Please identify issues and provide specific fixes for:
1. Code quality and Vue.js best practices
2. Accessibility and usability issues
3. Performance optimizations
4. Security considerations
5. Missing functionality or edge cases"""

        output_schema = {
            "validation_results": {
                "overall_score": "number (0-100)",
                "quality_grade": "string (A-F)",
                "critical_issues": ["string"],
                "recommendations": ["string"]
            },
            "code_fixes": [
                {
                    "file": "string",
                    "issue": "string",
                    "fix": "string",
                    "priority": "string (high/medium/low)"
                }
            ],
            "missing_features": [
                {
                    "feature": "string",
                    "importance": "string",
                    "implementation": "string"
                }
            ],
            "performance_optimizations": ["string"],
            "accessibility_improvements": ["string"]
        }
        
        return PromptTemplate(
            system_prompt=system_prompt,
            user_prompt_template=user_prompt_template,
            output_schema=output_schema,
            temperature=0.2,
            max_tokens=3000
        )

def get_prompt_by_stage(stage: str) -> PromptTemplate:
    """Get prompt template for a specific generation stage"""
    
    prompts = {
        "design_brief": AIPrompts.get_design_brief_prompt(),
        "architecture": AIPrompts.get_architecture_prompt(), 
        "component_generation": AIPrompts.get_component_generation_prompt(),
        "integration": AIPrompts.get_integration_prompt(),
        "validation": AIPrompts.get_validation_prompt()
    }
    
    if stage not in prompts:
        raise ValueError(f"Unknown stage: {stage}. Available: {list(prompts.keys())}")
    
    return prompts[stage]

def format_prompt(template: PromptTemplate, **kwargs) -> str:
    """Format a prompt template with provided variables"""
    return template.user_prompt_template.format(**kwargs) 