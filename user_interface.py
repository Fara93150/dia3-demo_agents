import streamlit as st 
from llm_agent import ConversationAgent
from speech_to_text import SpeechToText


class UserInterface:
	def __init__(self):
		st.set_page_config(page_title="Jarvis")
		st.title("Barbe-Quasar")
		self.conversation_agent_object = self.get_persistant_conversation_agent()
		self.speech_to_text_object = self.get_persistant_speech_to_text()


	def get_persistant_conversation_agent(self):

		if "conversation_agent_object" not in st.session_state:
			st.session_state.conversation_agent_object = ConversationAgent()

		return st.session_state.conversation_agent_object


	def get_persistant_speech_to_text(self):

		if "speech_to_text_object" not in st.session_state:
			st.session_state.speech_to_text_object = SpeechToText()

		return st.session_state.speech_to_text_object


	def show_discussion_history(self):
		for message in self.conversation_agent_object.get_conversation_history():
			with st.chat_message(message["role"]):
				st.markdown(message["content"])


	def run(self):
		interaction = st.chat_input(
			"Que veux tu moussaillon ?",
			accept_file=False,
			accept_audio=True
			)

		if interaction :
			# vocal -> on transcrit l'audio en texte, sinon on prend le texte tapé
			if interaction.audio :
				try :
					text_interaction = self.speech_to_text_object.transcribe(interaction.audio)
				except Exception as error :
					st.error(f"Impossible de transcrire le vocal : {error}")
					text_interaction = ""
			else :
				text_interaction = interaction.text

			# on ignore un message vide (ex : vocal silencieux)
			if text_interaction and text_interaction.strip() :
				self.conversation_agent_object.ask_llm(text_interaction.strip())

		self.show_discussion_history()


if __name__ == "__main__":
	user_interface_object = UserInterface()
	user_interface_object.run()






































	# response = ask_llm(user_input)
	# with st.chat_message("user"):
	# 	st.markdown(user_input)

	# with st.chat_message("system"):
	# 	st.markdown(response)


