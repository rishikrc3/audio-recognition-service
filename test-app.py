import requests
import unittest
import io

BASE_URL = "http://localhost:5002/recognize"

class TestRecognitionService(unittest.TestCase):

    def test_recognize_success(self):
       
        with open("/Users/rishik/Desktop/Catelogue/wavs/~Blinding Lights.wav", "rb") as f:
            files = {"file": ("Blinding_Lights.wav", f, "audio/wav")}
            rsp = requests.post(BASE_URL, files=files)
        self.assertEqual(rsp.status_code, 200)
        self.assertEqual(rsp.headers["Content-Type"], "audio/wav")
        self.assertGreater(len(rsp.content), 0)  # Ensure response contains audio data

    def test_recognize_no_file(self):
        rsp = requests.post(BASE_URL)
        self.assertEqual(rsp.status_code, 400)
        self.assertIn("No file uploaded", rsp.json()["error"])

    # def test_recognize_empty_file(self):
    #     files = {"file": ("empty.mp3", io.BytesIO(b""), "audio/mpeg")}
    #     rsp = requests.post(BASE_URL, files=files)
    #     self.assertEqual(rsp.status_code, 404)
    #     self.assertIn("No file selected", rsp.json()["error"])

    # def test_recognize_audd_api_failure(self):
    #     """❌ Test when AudD API is down."""
    #     with open("/Users/rishik/Desktop/Recognition/test_audio.wav", "rb") as f:
    #         files = {"file": ("test_audio.wav", f, "audio/wav")}
    #         rsp = requests.post(BASE_URL, files=files)
        
    #     self.assertEqual(rsp.status_code, 500)
    #     self.assertIn("AudD API request failed", rsp.json()["error"])

    # def test_recognize_track_not_found(self):
    #     """❌ Test when AudD API does not recognize the track."""
    #     with open("/Users/rishik/Desktop/Recognition/unknown_audio.wav", "rb") as f:
    #         files = {"file": ("unknown_audio.wav", f, "audio/wav")}
    #         rsp = requests.post(BASE_URL, files=files)
        
    #     self.assertEqual(rsp.status_code, 404)
    #     self.assertIn("Track not recognized", rsp.json()["error"])

    # def test_recognize_track_not_in_catalog(self):
    #     """❌ Test when track is recognized but not found in the catalog."""
    #     with open("/Users/rishik/Desktop/Recognition/recognized_but_missing.wav", "rb") as f:
    #         files = {"file": ("recognized_but_missing.wav", f, "audio/wav")}
    #         rsp = requests.post(BASE_URL, files=files)
        
    #     self.assertEqual(rsp.status_code, 404)
    #     self.assertIn("Track not recognized or not found", rsp.json()["error"])

    # def test_recognize_catalog_service_failure(self):
    #     """❌ Test when track is recognized but catalog service is down."""
    #     with open("/Users/rishik/Desktop/Recognition/test_audio.wav", "rb") as f:
    #         files = {"file": ("test_audio.wav", f, "audio/wav")}
    #         rsp = requests.post(BASE_URL, files=files)
        
    #     self.assertEqual(rsp.status_code, 500)
    #     self.assertIn("Track retrieval failed", rsp.json()["error"])

if __name__ == "__main__":
    unittest.main()
