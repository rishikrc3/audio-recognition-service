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

    #yet to be tested, failing
    # def test_recognize_empty_file(self):
    #     files = {"file": ("empty.mp3", io.BytesIO(b""), "audio/mpeg")}
    #     rsp = requests.post(BASE_URL, files=files)
    #     self.assertEqual(rsp.status_code, 404)
    #     self.assertIn("No file selected", rsp.json()["error"])

   
    def test_recognize_track_not_found(self):
        with open("/Users/rishik/Desktop/Catelogue/wavs/~Davos.wav", "rb") as f:
            files = {"file": ("unknown_audio.wav", f, "audio/wav")}
            rsp = requests.post(BASE_URL, files=files)
        
        self.assertEqual(rsp.status_code, 404)
        self.assertIn("Track not recognized", rsp.json()["error"])

    def test_recognize_track_not_in_catalog(self):
       
        with open("/Users/rishik/Desktop/Catelogue/wavs/~Don't Look Back In Anger.wav", "rb") as f:
            files = {"file": ("recognized_but_missing.wav", f, "audio/wav")}
            rsp = requests.post(BASE_URL, files=files)
        
        self.assertEqual(rsp.status_code, 404)
        self.assertIn("Track recognized but not found", rsp.json()["error"])

    def test_recognize_invalid_file_type(self):
        with open("/Users/rishik/Desktop/Catelogue/wavs/catelog.py", "rb") as f:
            files = {"file": ("test_image.png", f, "image/png")}  
            rsp = requests.post(BASE_URL, files=files)
        
        self.assertEqual(rsp.status_code, 415) 
        self.assertIn("Invalid file type", rsp.json()["error"])


if __name__ == "__main__":
    unittest.main()
