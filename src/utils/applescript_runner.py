"""
AppleScript runner utilities
"""

import subprocess
import json
from pathlib import Path
from typing import Any, Optional
import os
import tempfile

from .error_handler import AppleScriptError


class AppleScriptRunner:
    """AppleScript executor"""
    
    def __init__(self, script_dir: Optional[Path] = None) -> None:
        """
        Initialize AppleScript executor
        
        Args:
            script_dir: AppleScript script directory path
        """
        if script_dir is None:
            # Default script directory
            current_dir = Path(__file__).parent.parent
            script_dir = current_dir / "applescript"
        
        self.script_dir = Path(script_dir)
        self._ensure_script_dir()
    
    def _ensure_script_dir(self) -> None:
        """Ensure script directory exists"""
        if not self.script_dir.exists():
            self.script_dir.mkdir(parents=True, exist_ok=True)
    
    def run_script(self, script_name: str, function_name: str, *args) -> str:
        """
        Run specified function in AppleScript script
        
        Args:
            script_name: Script file name (without extension)
            function_name: Function name
            *args: Function parameters
            
        Returns:
            Script execution result
            
        Raises:
            AppleScriptError: Script execution error
        """
        # Try .scpt first, then .applescript
        script_path = self.script_dir / f"{script_name}.scpt"
        if not script_path.exists():
            script_path = self.script_dir / f"{script_name}.applescript"
        
        if not script_path.exists():
            raise AppleScriptError(f"Script file not found: {script_name} (tried .scpt and .applescript)")
        
        # If it's a .applescript file, read and execute directly
        if script_path.suffix == '.applescript':
            return self._execute_applescript_file(script_path, function_name, *args)
        
        # For .scpt files, use the original method
        script_args = self._format_args(*args)
        
        try:
            # Build osascript command
            cmd = [
                "osascript",
                str(script_path),
                function_name
            ] + script_args
            
            # Execute script
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            return result.stdout.strip()
            
        except subprocess.CalledProcessError as e:
            raise AppleScriptError(f"AppleScript execution failed: {e.stderr.strip()}")
        except Exception as e:
            raise AppleScriptError(f"Unexpected error during script execution: {str(e)}")
    
    def _execute_applescript_file(self, script_path: Path, function_name: str, *args) -> str:
        """
        Execute AppleScript file directly
        
        Returns:
            Script execution result
        """
        try:
            # Execute AppleScript code
            script_content = script_path.read_text(encoding='utf-8')
            return self.execute_script(script_content)
            
        except Exception as e:
            raise AppleScriptError(f"Failed to execute AppleScript file: {str(e)}")
    
    def execute_script(self, script_code: str) -> str:
        """
        Execute AppleScript code
        
        Args:
            script_code: AppleScript code
            
        Returns:
            Execution result
        """
        try:
            # Use osascript to execute AppleScript
            result = subprocess.run(
                ["osascript", "-e", script_code],
                capture_output=True,
                text=True,
                check=True
            )
            
            return result.stdout.strip()
            
        except subprocess.CalledProcessError as e:
            raise AppleScriptError(f"AppleScript execution failed: {e.stderr.strip()}")
        except Exception as e:
            raise AppleScriptError(f"Unexpected error during script execution: {str(e)}")
    
    def run_function(self, script_file: str, function_name: str, args: list) -> str:
        """
        Run a specific function from an AppleScript file with arguments
        
        Args:
            script_file: AppleScript file name (with extension)
            function_name: Function name to call
            args: List of arguments to pass to the function
            
        Returns:
            Script execution result
        """
        script_path = self.script_dir / script_file
        
        if not script_path.exists():
            raise AppleScriptError(f"Script file not found: {script_file}")
        
        try:
            # Read the script content
            script_content = script_path.read_text(encoding='utf-8')
            
            # Format the arguments for AppleScript
            formatted_args = []
            for arg in args:
                if isinstance(arg, str):
                    # Escape quotes in string arguments
                    escaped_arg = arg.replace('"', '\\"')
                    formatted_args.append(f'"{escaped_arg}"')
                elif isinstance(arg, (int, float)):
                    formatted_args.append(str(arg))
                elif isinstance(arg, bool):
                    formatted_args.append("true" if arg else "false")
                elif arg is None or arg == "":
                    formatted_args.append('""')
                else:
                    formatted_args.append(str(arg))
            
            # Create the function call
            args_str = ", ".join(formatted_args)
            function_call = f"{function_name}({args_str})"
            
            # Combine script content with function call
            full_script = f"{script_content}\n\n{function_call}"
            
            # Execute the script
            return self.execute_script(full_script)
            
        except Exception as e:
            raise AppleScriptError(f"Failed to execute function {function_name} in {script_file}: {str(e)}")
    
    def run_inline_script(self, script_code: str) -> str:
        """
        Execute inline AppleScript code (alias for execute_script)
        
        Args:
            script_code: AppleScript code
            
        Returns:
            Execution result
        """
        return self.execute_script(script_code)
    
    def check_keynote_running(self) -> bool:
        """
        Check if Keynote application is running
        
        Returns:
            True if Keynote is running, False otherwise
        """
        try:
            script = '''
                tell application "System Events"
                    return (name of processes) contains "Keynote"
                end tell
            '''
            result = self.execute_script(script)
            return result.lower() == "true"
        except Exception:
            return False
    
    def launch_keynote(self) -> None:
        """
        Launch Keynote application
        
        Raises:
            AppleScriptError: If Keynote fails to launch
        """
        try:
            script = '''
                tell application "Keynote"
                    activate
                end tell
            '''
            self.execute_script(script)
        except Exception as e:
            raise AppleScriptError(f"Failed to launch Keynote: {str(e)}")
    
    def _format_args(self, *args) -> list[str]:
        """
        Format arguments for AppleScript
        
        Args:
            *args: Function arguments
            
        Returns:
            Formatted argument list
        """
        formatted_args = []
        for arg in args:
            if isinstance(arg, (dict, list)):
                # Convert complex objects to JSON strings
                formatted_args.append(json.dumps(arg))
            elif isinstance(arg, bool):
                # Convert boolean to AppleScript format
                formatted_args.append("true" if arg else "false")
            elif isinstance(arg, (int, float)):
                # Keep numbers as strings
                formatted_args.append(str(arg))
            elif arg is None:
                # Handle None values
                formatted_args.append("missing value")
            else:
                # Handle strings and other types
                formatted_args.append(str(arg))
        
        return formatted_args


# Global instance for easy access
applescript_runner = AppleScriptRunner()


def run_applescript(script_name: str, function_name: str, *args) -> str:
    """
    Convenience function to run AppleScript
    
    Args:
        script_name: Script file name (without extension)
        function_name: Function name
        *args: Function arguments
        
    Returns:
        Script execution result
    """
    return applescript_runner.run_script(script_name, function_name, *args)


def execute_applescript_code(script_code: str) -> str:
    """
    Convenience function to execute AppleScript code
    
    Args:
        script_code: AppleScript code
        
    Returns:
        Execution result
    """
    return applescript_runner.execute_script(script_code)