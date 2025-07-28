#!/usr/bin/env python3
"""
Website Validator for Generated Store Websites

Validates generated websites for:
- TypeScript compilation
- Vue.js syntax
- Design system compliance
- Responsive design
- Accessibility
- Performance
- Code quality
"""

import os
import json
import re
import subprocess
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class ValidationLevel(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

@dataclass
class ValidationResult:
    level: ValidationLevel
    category: str
    message: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    suggestion: Optional[str] = None

class WebsiteValidator:
    """Comprehensive validator for generated store websites"""
    
    def __init__(self, website_path: str):
        self.website_path = website_path
        self.results: List[ValidationResult] = []
        self.design_tokens = self._load_design_tokens()
        
    def _load_design_tokens(self) -> Dict[str, Any]:
        """Load design system tokens for validation"""
        try:
            tokens_path = os.path.join('generator', 'design_system', 'tokens.json')
            with open(tokens_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def validate_all(self) -> Dict[str, Any]:
        """Run all validations and return comprehensive results"""
        self.results = []
        
        print("🔍 Running comprehensive website validation...")
        
        # Core validations
        self._validate_file_structure()
        self._validate_package_json()
        self._validate_vue_syntax()
        self._validate_typescript()
        self._validate_design_system_compliance()
        self._validate_responsive_design()
        self._validate_accessibility()
        self._validate_performance()
        self._validate_seo()
        self._validate_security()
        
        # Generate report
        return self._generate_report()
    
    def _validate_file_structure(self):
        """Validate that all required files are present"""
        required_files = [
            'package.json',
            'index.html',
            'src/main.ts',
            'src/App.vue',
            'src/router/index.js',
            'tailwind.config.js',
            'vite.config.ts'
        ]
        
        required_dirs = [
            'src/components',
            'src/stores',
            'src/pages',
            'src/styles'
        ]
        
        for file_path in required_files:
            full_path = os.path.join(self.website_path, file_path)
            if not os.path.exists(full_path):
                self.results.append(ValidationResult(
                    level=ValidationLevel.ERROR,
                    category="File Structure",
                    message=f"Required file missing: {file_path}",
                    file_path=file_path,
                    suggestion=f"Create {file_path} with appropriate content"
                ))
        
        for dir_path in required_dirs:
            full_path = os.path.join(self.website_path, dir_path)
            if not os.path.exists(full_path):
                self.results.append(ValidationResult(
                    level=ValidationLevel.ERROR,
                    category="File Structure",
                    message=f"Required directory missing: {dir_path}",
                    file_path=dir_path,
                    suggestion=f"Create {dir_path} directory"
                ))
    
    def _validate_package_json(self):
        """Validate package.json for required dependencies"""
        package_path = os.path.join(self.website_path, 'package.json')
        
        if not os.path.exists(package_path):
            return
        
        try:
            with open(package_path, 'r') as f:
                package_data = json.load(f)
            
            required_deps = ['vue', 'vue-router', 'pinia']
            required_dev_deps = ['@vitejs/plugin-vue', 'typescript', 'vite']
            
            dependencies = package_data.get('dependencies', {})
            dev_dependencies = package_data.get('devDependencies', {})
            
            for dep in required_deps:
                if dep not in dependencies:
                    self.results.append(ValidationResult(
                        level=ValidationLevel.ERROR,
                        category="Dependencies",
                        message=f"Missing required dependency: {dep}",
                        file_path="package.json",
                        suggestion=f"Add {dep} to dependencies"
                    ))
            
            for dep in required_dev_deps:
                if dep not in dev_dependencies:
                    self.results.append(ValidationResult(
                        level=ValidationLevel.WARNING,
                        category="Dependencies",
                        message=f"Missing recommended dev dependency: {dep}",
                        file_path="package.json",
                        suggestion=f"Add {dep} to devDependencies"
                    ))
                    
        except json.JSONDecodeError:
            self.results.append(ValidationResult(
                level=ValidationLevel.ERROR,
                category="Dependencies",
                message="Invalid JSON in package.json",
                file_path="package.json",
                suggestion="Fix JSON syntax errors"
            ))
    
    def _validate_vue_syntax(self):
        """Validate Vue.js component syntax"""
        for root, dirs, files in os.walk(self.website_path):
            for file in files:
                if file.endswith('.vue'):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, self.website_path)
                    self._validate_vue_file(file_path, rel_path)
    
    def _validate_vue_file(self, file_path: str, rel_path: str):
        """Validate individual Vue file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for required sections
            if '<template>' not in content:
                self.results.append(ValidationResult(
                    level=ValidationLevel.ERROR,
                    category="Vue Syntax",
                    message="Missing <template> section",
                    file_path=rel_path,
                    suggestion="Add <template> section to Vue component"
                ))
            
            if '<script setup' not in content and '<script>' not in content:
                self.results.append(ValidationResult(
                    level=ValidationLevel.WARNING,
                    category="Vue Syntax",
                    message="Missing <script> section",
                    file_path=rel_path,
                    suggestion="Add <script setup> section for Composition API"
                ))
            
            # Check for TypeScript usage
            if '<script setup lang="ts">' not in content and '<script lang="ts">' not in content:
                self.results.append(ValidationResult(
                    level=ValidationLevel.INFO,
                    category="TypeScript",
                    message="Component not using TypeScript",
                    file_path=rel_path,
                    suggestion="Consider adding lang=\"ts\" to script tag"
                ))
            
            # Check for proper prop definitions
            if 'defineProps' in content and 'interface Props' not in content:
                self.results.append(ValidationResult(
                    level=ValidationLevel.WARNING,
                    category="TypeScript",
                    message="Props defined without TypeScript interface",
                    file_path=rel_path,
                    suggestion="Define Props interface for better type safety"
                ))
                
        except Exception as e:
            self.results.append(ValidationResult(
                level=ValidationLevel.ERROR,
                category="Vue Syntax",
                message=f"Error reading Vue file: {str(e)}",
                file_path=rel_path
            ))
    
    def _validate_typescript(self):
        """Validate TypeScript compilation"""
        tsconfig_path = os.path.join(self.website_path, 'tsconfig.json')
        
        if not os.path.exists(tsconfig_path):
            self.results.append(ValidationResult(
                level=ValidationLevel.WARNING,
                category="TypeScript",
                message="Missing tsconfig.json",
                file_path="tsconfig.json",
                suggestion="Create tsconfig.json for TypeScript configuration"
            ))
            return
        
        # Try to run TypeScript compiler check
        try:
            result = subprocess.run(
                ['npx', 'vue-tsc', '--noEmit'],
                cwd=self.website_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                self.results.append(ValidationResult(
                    level=ValidationLevel.ERROR,
                    category="TypeScript",
                    message="TypeScript compilation errors",
                    suggestion="Fix TypeScript errors before deployment"
                ))
                
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.results.append(ValidationResult(
                level=ValidationLevel.WARNING,
                category="TypeScript",
                message="Could not run TypeScript compiler",
                suggestion="Ensure vue-tsc is installed"
            ))
    
    def _validate_design_system_compliance(self):
        """Validate compliance with design system tokens"""
        if not self.design_tokens:
            return
        
        # Check CSS/SCSS files for design token usage
        for root, dirs, files in os.walk(self.website_path):
            for file in files:
                if file.endswith(('.css', '.scss', '.vue')):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, self.website_path)
                    self._validate_design_tokens_in_file(file_path, rel_path)
    
    def _validate_design_tokens_in_file(self, file_path: str, rel_path: str):
        """Check if file uses design tokens instead of hardcoded values"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for hardcoded colors (basic check)
            color_patterns = [
                r'#[0-9a-fA-F]{3,6}',  # Hex colors
                r'rgb\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)',  # RGB colors
                r'rgba\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*[\d.]+\s*\)'  # RGBA colors
            ]
            
            for pattern in color_patterns:
                matches = re.findall(pattern, content)
                if matches:
                    # Exclude common acceptable colors like #000, #fff
                    filtered_matches = [m for m in matches if m not in ['#000', '#fff', '#000000', '#ffffff']]
                    if filtered_matches:
                        self.results.append(ValidationResult(
                            level=ValidationLevel.WARNING,
                            category="Design System",
                            message=f"Hardcoded colors found: {', '.join(filtered_matches[:3])}",
                            file_path=rel_path,
                            suggestion="Use design system color tokens instead"
                        ))
                        break
            
            # Check for hardcoded spacing values
            spacing_pattern = r'(?:margin|padding|gap):\s*\d+px'
            if re.search(spacing_pattern, content):
                self.results.append(ValidationResult(
                    level=ValidationLevel.INFO,
                    category="Design System",
                    message="Hardcoded spacing values found",
                    file_path=rel_path,
                    suggestion="Consider using design system spacing tokens"
                ))
                
        except Exception as e:
            pass  # Skip files that can't be read
    
    def _validate_responsive_design(self):
        """Validate responsive design implementation"""
        for root, dirs, files in os.walk(self.website_path):
            for file in files:
                if file.endswith('.vue'):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, self.website_path)
                    self._validate_responsive_in_file(file_path, rel_path)
    
    def _validate_responsive_in_file(self, file_path: str, rel_path: str):
        """Check for responsive design patterns in Vue files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for responsive classes
            responsive_patterns = [
                r'sm:',
                r'md:',
                r'lg:',
                r'xl:',
                r'@media'
            ]
            
            has_responsive = any(re.search(pattern, content) for pattern in responsive_patterns)
            
            # If component has layout elements, it should be responsive
            layout_patterns = [
                r'grid',
                r'flex',
                r'container',
                r'w-full',
                r'h-full'
            ]
            
            has_layout = any(re.search(pattern, content) for pattern in layout_patterns)
            
            if has_layout and not has_responsive:
                self.results.append(ValidationResult(
                    level=ValidationLevel.WARNING,
                    category="Responsive Design",
                    message="Component with layout elements lacks responsive design",
                    file_path=rel_path,
                    suggestion="Add responsive classes (sm:, md:, lg:, xl:)"
                ))
                
        except Exception as e:
            pass
    
    def _validate_accessibility(self):
        """Validate accessibility features"""
        for root, dirs, files in os.walk(self.website_path):
            for file in files:
                if file.endswith('.vue'):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, self.website_path)
                    self._validate_accessibility_in_file(file_path, rel_path)
    
    def _validate_accessibility_in_file(self, file_path: str, rel_path: str):
        """Check accessibility features in Vue files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for images without alt text
            img_without_alt = re.findall(r'<img[^>]*(?!.*alt=)[^>]*>', content)
            if img_without_alt:
                self.results.append(ValidationResult(
                    level=ValidationLevel.ERROR,
                    category="Accessibility",
                    message="Images without alt text found",
                    file_path=rel_path,
                    suggestion="Add alt attributes to all images"
                ))
            
            # Check for buttons without accessible text
            if '<button' in content:
                button_pattern = r'<button[^>]*>[\s]*</button>'
                empty_buttons = re.findall(button_pattern, content)
                if empty_buttons:
                    self.results.append(ValidationResult(
                        level=ValidationLevel.WARNING,
                        category="Accessibility",
                        message="Empty buttons found",
                        file_path=rel_path,
                        suggestion="Add text content or aria-label to buttons"
                    ))
            
            # Check for form inputs without labels
            if '<input' in content and 'label' not in content.lower():
                self.results.append(ValidationResult(
                    level=ValidationLevel.WARNING,
                    category="Accessibility",
                    message="Form inputs may be missing labels",
                    file_path=rel_path,
                    suggestion="Associate labels with form inputs"
                ))
                
        except Exception as e:
            pass
    
    def _validate_performance(self):
        """Validate performance-related aspects"""
        # Check for potential performance issues
        self._check_large_bundles()
        self._check_image_optimization()
        self._check_lazy_loading()
    
    def _check_large_bundles(self):
        """Check for potentially large bundle sizes"""
        package_path = os.path.join(self.website_path, 'package.json')
        
        if os.path.exists(package_path):
            try:
                with open(package_path, 'r') as f:
                    package_data = json.load(f)
                
                dependencies = package_data.get('dependencies', {})
                heavy_libs = ['moment', 'lodash', 'jquery']
                
                for lib in heavy_libs:
                    if lib in dependencies:
                        self.results.append(ValidationResult(
                            level=ValidationLevel.WARNING,
                            category="Performance",
                            message=f"Heavy library detected: {lib}",
                            file_path="package.json",
                            suggestion=f"Consider lighter alternatives to {lib}"
                        ))
                        
            except json.JSONDecodeError:
                pass
    
    def _check_image_optimization(self):
        """Check for image optimization"""
        for root, dirs, files in os.walk(self.website_path):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    file_path = os.path.join(root, file)
                    file_size = os.path.getsize(file_path)
                    
                    # Warn about large images (>500KB)
                    if file_size > 500 * 1024:
                        rel_path = os.path.relpath(file_path, self.website_path)
                        self.results.append(ValidationResult(
                            level=ValidationLevel.WARNING,
                            category="Performance",
                            message=f"Large image file: {file} ({file_size // 1024}KB)",
                            file_path=rel_path,
                            suggestion="Optimize image size and consider WebP format"
                        ))
    
    def _check_lazy_loading(self):
        """Check for lazy loading implementation"""
        for root, dirs, files in os.walk(self.website_path):
            for file in files:
                if file.endswith('.vue'):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, self.website_path)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Check for images without lazy loading
                        img_tags = re.findall(r'<img[^>]*>', content)
                        for img_tag in img_tags:
                            if 'loading="lazy"' not in img_tag and 'loading="eager"' not in img_tag:
                                self.results.append(ValidationResult(
                                    level=ValidationLevel.INFO,
                                    category="Performance",
                                    message="Image without loading attribute",
                                    file_path=rel_path,
                                    suggestion="Add loading=\"lazy\" for better performance"
                                ))
                                break
                                
                    except Exception:
                        pass
    
    def _validate_seo(self):
        """Validate SEO-related aspects"""
        index_path = os.path.join(self.website_path, 'index.html')
        
        if os.path.exists(index_path):
            try:
                with open(index_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for meta tags
                if '<meta name="description"' not in content:
                    self.results.append(ValidationResult(
                        level=ValidationLevel.WARNING,
                        category="SEO",
                        message="Missing meta description",
                        file_path="index.html",
                        suggestion="Add meta description for better SEO"
                    ))
                
                if '<title>' not in content:
                    self.results.append(ValidationResult(
                        level=ValidationLevel.ERROR,
                        category="SEO",
                        message="Missing page title",
                        file_path="index.html",
                        suggestion="Add descriptive page title"
                    ))
                    
            except Exception:
                pass
    
    def _validate_security(self):
        """Validate security aspects"""
        # Check for potential security issues
        for root, dirs, files in os.walk(self.website_path):
            for file in files:
                if file.endswith(('.js', '.ts', '.vue')):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, self.website_path)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Check for potential XSS vulnerabilities
                        if 'innerHTML' in content:
                            self.results.append(ValidationResult(
                                level=ValidationLevel.WARNING,
                                category="Security",
                                message="innerHTML usage detected",
                                file_path=rel_path,
                                suggestion="Use textContent or Vue's v-html with caution"
                            ))
                        
                        # Check for exposed API keys
                        api_key_pattern = r'(?:api_key|apikey|access_key)[\s]*[:=][\s]*[\'"][a-zA-Z0-9]{10,}[\'"]'
                        if re.search(api_key_pattern, content, re.IGNORECASE):
                            self.results.append(ValidationResult(
                                level=ValidationLevel.ERROR,
                                category="Security",
                                message="Potential exposed API key",
                                file_path=rel_path,
                                suggestion="Move API keys to environment variables"
                            ))
                            
                    except Exception:
                        pass
    
    def _generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive validation report"""
        errors = [r for r in self.results if r.level == ValidationLevel.ERROR]
        warnings = [r for r in self.results if r.level == ValidationLevel.WARNING]
        info = [r for r in self.results if r.level == ValidationLevel.INFO]
        
        # Calculate score
        max_score = 100
        error_penalty = len(errors) * 10
        warning_penalty = len(warnings) * 3
        info_penalty = len(info) * 1
        
        score = max(0, max_score - error_penalty - warning_penalty - info_penalty)
        
        # Determine grade
        if score >= 90:
            grade = "A"
        elif score >= 80:
            grade = "B"
        elif score >= 70:
            grade = "C"
        elif score >= 60:
            grade = "D"
        else:
            grade = "F"
        
        # Group results by category
        by_category = {}
        for result in self.results:
            if result.category not in by_category:
                by_category[result.category] = []
            by_category[result.category].append(result)
        
        return {
            "summary": {
                "score": score,
                "grade": grade,
                "total_issues": len(self.results),
                "errors": len(errors),
                "warnings": len(warnings),
                "info": len(info)
            },
            "results_by_level": {
                "errors": [self._result_to_dict(r) for r in errors],
                "warnings": [self._result_to_dict(r) for r in warnings],
                "info": [self._result_to_dict(r) for r in info]
            },
            "results_by_category": {
                category: [self._result_to_dict(r) for r in results]
                for category, results in by_category.items()
            },
            "recommendations": self._generate_recommendations(score, by_category)
        }
    
    def _result_to_dict(self, result: ValidationResult) -> Dict[str, Any]:
        """Convert ValidationResult to dictionary"""
        return {
            "level": result.level.value,
            "category": result.category,
            "message": result.message,
            "file_path": result.file_path,
            "line_number": result.line_number,
            "suggestion": result.suggestion
        }
    
    def _generate_recommendations(self, score: int, by_category: Dict[str, List[ValidationResult]]) -> List[str]:
        """Generate actionable recommendations based on validation results"""
        recommendations = []
        
        if score < 70:
            recommendations.append("🚨 Critical: Address all error-level issues before deployment")
        
        if "File Structure" in by_category:
            recommendations.append("📁 Ensure all required files and directories are present")
        
        if "TypeScript" in by_category:
            recommendations.append("🔧 Fix TypeScript compilation errors for better code quality")
        
        if "Accessibility" in by_category:
            recommendations.append("♿ Improve accessibility for better user experience")
        
        if "Performance" in by_category:
            recommendations.append("⚡ Optimize performance for faster load times")
        
        if "Security" in by_category:
            recommendations.append("🔒 Address security vulnerabilities immediately")
        
        if score >= 90:
            recommendations.append("✅ Excellent! Your website meets high quality standards")
        elif score >= 80:
            recommendations.append("👍 Good quality! Address remaining warnings for even better results")
        
        return recommendations

def validate_website(website_path: str) -> Dict[str, Any]:
    """Main function to validate a generated website"""
    validator = WebsiteValidator(website_path)
    return validator.validate_all()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python website_validator.py <website_path>")
        sys.exit(1)
    
    website_path = sys.argv[1]
    report = validate_website(website_path)
    
    print(f"\n🎯 Validation Score: {report['summary']['score']}/100 (Grade: {report['summary']['grade']})")
    print(f"📊 Issues Found: {report['summary']['total_issues']} total")
    print(f"   - ❌ Errors: {report['summary']['errors']}")
    print(f"   - ⚠️  Warnings: {report['summary']['warnings']}")
    print(f"   - ℹ️  Info: {report['summary']['info']}")
    
    if report['recommendations']:
        print("\n💡 Recommendations:")
        for rec in report['recommendations']:
            print(f"   {rec}") 