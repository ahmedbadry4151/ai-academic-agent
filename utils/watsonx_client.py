import os
from dotenv import load_dotenv
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.foundation_models.utils.enums import ModelTypes

load_dotenv()

class WatsonxClient:
    def __init__(self):
        self.api_key = os.getenv("WATSONX_API_KEY", "your_api_key")
        self.project_id = os.getenv("WATSONX_PROJECT_ID", "your_project_id")
        self.url = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
        
        if self.api_key == "your_api_key":
             print("Warning: WATSONX_API_KEY not set in environment variables.")

        self.credentials = {
            "url": self.url,
            "apikey": self.api_key
        }
        
        # Default parameters
        self.params = {
            GenParams.DECODING_METHOD: "greedy",
            GenParams.MAX_NEW_TOKENS: 4000,
            GenParams.MIN_NEW_TOKENS: 1,
            GenParams.REPETITION_PENALTY: 1.1
        }
        
        # You can make the model configurable
        # Using a model from the supported list for this environment
        self.model_id = "ibm/granite-3-8b-instruct"
       

    def generate_text(self, prompt, model_id=None):
        """
        Generate text using Watsonx.ai
        """
        try:
            print(f"[WatsonX] Using model: {model_id if model_id else self.model_id}")
            print(f"[WatsonX] Project ID: {self.project_id}")
            print(f"[WatsonX] Prompt length: {len(prompt)} chars")
            
            model = ModelInference(
                model_id=model_id if model_id else self.model_id,
                params=self.params,
                credentials=self.credentials,
                project_id=self.project_id
            )
            
            response = model.generate_text(prompt=prompt)
            
            if response:
                print(f"[WatsonX] Response received: {len(response)} chars")
            else:
                print("[WatsonX] WARNING: Empty response received")
                
            return response if response else "Error: Empty response from Watsonx"
            
        except Exception as e:
            error_msg = f"Error connecting to Watsonx: {str(e)}"
            print(f"[WatsonX] ERROR: {error_msg}")
            import traceback
            traceback.print_exc()
            return error_msg
