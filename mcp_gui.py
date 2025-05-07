from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QWidget, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
import asyncio
from pydantic_ai import Agent
import mcp_client
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_gla import GoogleGLAProvider
from qasync import QEventLoop, asyncSlot

class AgentWorker(QThread):
    response_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, agent, user_input):
        super().__init__() 
        self.agent = agent
        self.user_input = user_input

    async def run_agent(self):
        try:
            result = await self.agent.run(self.user_input)
            self.response_signal.emit(result.output)
        except Exception as e:
            self.error_signal.emit(str(e))

    def run(self):
        asyncio.run(self.run_agent())

# Ensure the asyncio event loop is properly managed
class MCPApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MCP Application")
        self.setGeometry(100, 100, 800, 600)

        self.agent = None

        # Main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Output text area
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.layout.addWidget(self.output_text)

        # Input field
        self.input_field = QLineEdit()
        self.layout.addWidget(self.input_field)

        # Send button
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.handle_user_input)
        self.layout.addWidget(self.send_button)

        # Schedule the agent initialization
        QTimer.singleShot(0, self.initialize_agent)

    @asyncSlot()
    async def initialize_agent(self):
        try:
            client = mcp_client.MCPClient()
            client.load_servers("GhidraMCP.json")
            tools = await client.start()
            model = GeminiModel(
                'gemini-2.0-flash', provider=GoogleGLAProvider(api_key='AIzaSyAYXNByPMyooQTZDig21a088vAus0bnV0I')
            )
            self.agent = Agent(model, tools=tools)
            self.output_text.append("Agent initialized successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to initialize agent: {e}")

    @asyncSlot()
    async def handle_user_input(self):
        user_input = self.input_field.text()
        if not user_input.strip():
            return

        self.output_text.append(f"[You]: {user_input}")
        self.input_field.clear()

        if self.agent:
            try:
                result = await self.agent.run(user_input)
                self.output_text.append(f"[" + self.agent.model.model_name + "]: " + result.output)
            except Exception as e:
                self.output_text.append(f"[Error]: {e}")

# Update the main function to avoid using asyncio.run
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    # Use QEventLoop to integrate asyncio with PyQt5
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = MCPApp()
    window.show()

    with loop:
        loop.run_forever()