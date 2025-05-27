from datetime import datetime


class FileLogger:
    """Class for logging errors to a file."""
    def __init__(self, log_file: str):
        """Initialize the logger with a log file path."""
        self.log_file = log_file

    def log_error(self, message: str) -> None:
        """Log an error message to the file with a timestamp."""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as file:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                file.write(f"[{timestamp}] {message}\n")
        except IOError as e:
            print(f"Ошибка записи в лог: {e}")