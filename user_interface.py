import streamlit as st 
import base64
from llm_agent import ConversationAgent


class UserInterface:
	def __init__(self):
		st.set_page_config(page_title="Jarvis")
		st.title("Jarvis")
		self.conversation_agent_object = self.get_persistant_conversation_agent()


	def get_persistant_conversation_agent(self):
		
		if "conversation_agent_object" not in st.session_state:
			st.session_state.conversation_agent_object = ConversationAgent()

		return st.session_state.conversation_agent_object


	def show_discussion_history(self):
		for message in self.conversation_agent_object.get_conversation_history():
			with st.chat_message(message["role"]):
				content = message["content"]

				# Cas 1 : message texte simple
				if isinstance(content, str):
					st.markdown(content)

				# Cas 2 : liste de morceaux (texte et/ou image)
				else:
					for part in content:
						if part["type"] == "text":
							st.markdown(part["text"])
						elif part["type"] == "image_url":
							url = part["image_url"]["url"]           # "data:image/jpeg;base64,xxxx"
							image_base64 = url.split(",")[1]          # on garde seulement "xxxx"
							st.image(base64.b64decode(image_base64))  # base64 -> octets -> image


	def run(self):
		user_interaction = st.chat_input(
			"Que veux tu moussaillon ?",
			accept_file=True,
			accept_audio=True,
			file_type=["jpg", "jpeg", "png"],
			)

		if user_interaction :
			if user_interaction.audio:
				text_interaction = self.conversation_agent_object.transcribe(user_interaction.audio.getvalue())
			else:
				text_interaction = user_interaction.text

			image = user_interaction.files[0].getvalue() if user_interaction.files else None

			self.conversation_agent_object.ask_llm(text_interaction, image)
			self.show_discussion_history()



if __name__ == "__main__":
	user_interface_object = UserInterface()
	user_interface_object.run()








































	# response = ask_llm(user_input)
	# with st.chat_message("user"):
	# 	st.markdown(user_input)

	# with st.chat_message("system"):
	# 	st.markdown(response)


