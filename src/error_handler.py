"""
Error handling utilities for Dungeons & Daemons.
Provides comprehensive error handling and user feedback.
"""

import os
import traceback
from typing import Optional, Callable, Any
from enum import Enum

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.text import Text

from ascii_art import Colors


class ErrorType(Enum):
    """Types of errors that can occur in the game."""
    AI_CONNECTION = "ai_connection"
    AI_RESPONSE = "ai_response"
    SAVE_LOAD = "save_load"
    SETTINGS = "settings"
    USER_INPUT = "user_input"
    SYSTEM = "system"
    NETWORK = "network"


class ErrorHandler:
    """Handles errors gracefully with user-friendly messages."""
    
    def __init__(self, console: Console, debug_mode: bool = False):
        self.console = console
        self.debug_mode = debug_mode
        self.error_count = 0
        self.last_error = None
    
    def handle_error(self, error: Exception, error_type: ErrorType, 
                    context: str = "", retry_callback: Optional[Callable] = None) -> bool:
        """
        Handle an error with appropriate user feedback.
        
        Args:
            error: The exception that occurred
            error_type: Type of error for specific handling
            context: Additional context about when the error occurred
            retry_callback: Function to call if user wants to retry
            
        Returns:
            True if error was handled and should continue, False if should abort
        """
        self.error_count += 1
        self.last_error = error
        
        # Get error-specific message
        user_message, suggestions = self._get_error_message(error, error_type, context)
        
        # Show error to user
        self._display_error(user_message, suggestions, error if self.debug_mode else None)
        
        # Handle specific error types
        return self._handle_error_type(error_type, retry_callback)
    
    def _get_error_message(self, error: Exception, error_type: ErrorType, context: str) -> tuple[str, list[str]]:
        """Get user-friendly error message and suggestions."""
        
        if error_type == ErrorType.AI_CONNECTION:
            return (
                "Unable to connect to the AI Dungeon Master",
                [
                    "Make sure Ollama is running (ollama serve)",
                    "Check if your AI model is available (ollama list)",
                    "Verify the Ollama host and port in Settings",
                    "Try restarting Ollama service"
                ]
            )
        
        elif error_type == ErrorType.AI_RESPONSE:
            return (
                "The AI Dungeon Master seems confused",
                [
                    "The AI might be overloaded - try again",
                    "Consider switching to a different model in Settings",
                    "Check if Ollama has enough memory available",
                    "Try simplifying your action description"
                ]
            )
        
        elif error_type == ErrorType.SAVE_LOAD:
            return (
                "Problem with save file",
                [
                    "Check if the save directory exists and is writable",
                    "Verify you have enough disk space",
                    "The save file might be corrupted",
                    "Try creating a new character if loading fails"
                ]
            )
        
        elif error_type == ErrorType.SETTINGS:
            return (
                "Configuration issue detected",
                [
                    "Settings file might be corrupted",
                    "Try resetting to default settings",
                    "Check file permissions in the game directory",
                    "Verify the settings format is valid"
                ]
            )
        
        elif error_type == ErrorType.USER_INPUT:
            return (
                "Input processing error",
                [
                    "Try rephrasing your action",
                    "Avoid special characters or very long text",
                    "Make sure your action is clear and specific"
                ]
            )
        
        elif error_type == ErrorType.NETWORK:
            return (
                "Network connectivity issue",
                [
                    "Check your internet connection",
                    "Verify Ollama server is reachable",
                    "Check firewall settings",
                    "Try restarting the network service"
                ]
            )
        
        else:  # SYSTEM or unknown
            return (
                "Unexpected system error occurred",
                [
                    "Try restarting the game",
                    "Check system resources (memory, disk space)",
                    "Verify file permissions",
                    "Report this issue if it persists"
                ]
            )
    
    def _display_error(self, message: str, suggestions: list[str], error: Optional[Exception] = None):
        """Display error information to the user."""
        
        # Main error message
        error_panel = Panel(
            message,
            title=f"[{Colors.ERROR}]Error Encountered[/{Colors.ERROR}]",
            border_style=Colors.ERROR,
            padding=(1, 2)
        )
        self.console.print(error_panel)
        
        # Suggestions
        if suggestions:
            suggestion_text = "\n".join(f"• {suggestion}" for suggestion in suggestions)
            suggestion_panel = Panel(
                suggestion_text,
                title=f"[{Colors.INFO}]Suggestions[/{Colors.INFO}]",
                border_style=Colors.INFO,
                padding=(1, 2)
            )
            self.console.print(suggestion_panel)
        
        # Debug information if enabled
        if error and self.debug_mode:
            debug_info = f"Error Type: {type(error).__name__}\nMessage: {str(error)}"
            if hasattr(error, '__traceback__'):
                debug_info += f"\n\nTraceback:\n{''.join(traceback.format_tb(error.__traceback__))}"
            
            debug_panel = Panel(
                debug_info,
                title=f"[{Colors.WARNING}]Debug Information[/{Colors.WARNING}]",
                border_style=Colors.WARNING,
                padding=(1, 2)
            )
            self.console.print(debug_panel)
    
    def _handle_error_type(self, error_type: ErrorType, retry_callback: Optional[Callable]) -> bool:
        """Handle specific error types with appropriate actions."""
        
        # For critical errors, offer retry or exit
        if error_type in [ErrorType.AI_CONNECTION, ErrorType.SAVE_LOAD]:
            if retry_callback:
                if Confirm.ask(f"[{Colors.WARNING}]Would you like to try again?[/{Colors.WARNING}]", default=True):
                    try:
                        return retry_callback()
                    except Exception as e:
                        self.console.print(f"[{Colors.ERROR}]Retry failed: {e}[/{Colors.ERROR}]")
                        return False
            
            return Confirm.ask(f"[{Colors.WARNING}]Continue anyway?[/{Colors.WARNING}]", default=False)
        
        # For non-critical errors, just continue
        elif error_type in [ErrorType.AI_RESPONSE, ErrorType.USER_INPUT]:
            Prompt.ask("\nPress Enter to continue...")
            return True
        
        # For settings/system errors, offer to continue or exit
        else:
            return Confirm.ask(f"[{Colors.WARNING}]Continue despite this error?[/{Colors.WARNING}]", default=True)
    
    def show_error_summary(self):
        """Show summary of errors encountered during session."""
        if self.error_count == 0:
            return
        
        summary = f"Session encountered {self.error_count} error(s)"
        if self.last_error:
            summary += f"\nLast error: {type(self.last_error).__name__}"
        
        summary_panel = Panel(
            summary,
            title=f"[{Colors.WARNING}]Error Summary[/{Colors.WARNING}]",
            border_style=Colors.WARNING
        )
        self.console.print(summary_panel)
    
    def reset_error_count(self):
        """Reset the error counter."""
        self.error_count = 0
        self.last_error = None


def safe_execute(func: Callable, error_handler: ErrorHandler, 
                error_type: ErrorType, context: str = "", 
                retry_callback: Optional[Callable] = None) -> tuple[bool, Any]:
    """
    Safely execute a function with error handling.
    
    Args:
        func: Function to execute
        error_handler: ErrorHandler instance
        error_type: Type of error expected
        context: Context description
        
    Returns:
        Tuple of (success: bool, result: Any)
    """
    try:
        result = func()
        return True, result
    except Exception as e:
        handled = error_handler.handle_error(e, error_type, context, retry_callback)
        return handled, None


def validate_ollama_connection(host: str = "localhost", port: int = 11434) -> bool:
    """Validate that Ollama is accessible."""
    try:
        import requests
        import json
        
        url = f"http://{host}:{port}/api/tags"
        response = requests.get(url, timeout=5)
        return response.status_code == 200
        
    except Exception:
        return False 