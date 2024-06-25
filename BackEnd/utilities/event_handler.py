import openai
from BackEnd.utilities.image_generator import generate_image
from openai import AssistantEventHandler

client = openai.OpenAI()
class EventHandler(AssistantEventHandler):
                 def __init__(self):
                    self.full_text = ""
                    super().__init__()
                 def on_event(self, event):
                    # Retrieve events that are denoted with 'requires_action'
                     # since these will have our tool_calls
                    if event.event == 'thread.run.requires_action':
                        run_id = event.data.id  # Retrieve the run ID from the event data
                        print(run_id)
                        self.handle_requires_action(event.data, run_id)
    
                 def handle_requires_action(self, data, run_id):
                    tool_outputs = []
                    for tool in data.required_action.submit_tool_outputs.tool_calls:    
                
                        if tool.function.name == "generate_image":
                            print(tool.function.arguments)
                            output = generate_image(tool.function.arguments)
                            tool_outputs.append({"tool_call_id": tool.id, "output": output})
                        else:
                            raise ValueError(f"Unknown tool: {tool.function.name}")
                
                        # Submit all tool_outputs at the same time
                    self.submit_tool_outputs(tool_outputs, run_id)
                 def submit_tool_outputs(self, tool_outputs, run_id):
                        # Use the submit_tool_outputs_stream helper
                    
                    with client.beta.threads.runs.submit_tool_outputs_stream(
                        thread_id=self.current_run.thread_id,
                            run_id=self.current_run.id,
                        tool_outputs=tool_outputs,
                        ) as stream:
                            for event in stream:
                                if event.event == "thread.message.delta" and event.data.delta.content:
                                    self.full_text += event.data.delta.content[0].text.value