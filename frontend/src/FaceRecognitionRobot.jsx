import React, { useState, useEffect } from "react";
import { Camera, User, Activity } from "lucide-react";

export default function FaceRecognitionRobot() {
  const [isScanning, setIsScanning] = useState(false);
  const [recognitionStatus, setRecognitionStatus] = useState("idle");
  const [eyePosition, setEyePosition] = useState({ x: 0, y: 0 });
  const [detectedUser, setDetectedUser] = useState("");
  const [emotion, setEmotion] = useState("");

  // Eye animation
  useEffect(() => {
    if (isScanning) {
      const eyeInterval = setInterval(() => {
        setEyePosition({
          x: Math.sin(Date.now() / 200) * 8,
          y: Math.cos(Date.now() / 300) * 5,
        });
      }, 50);
      return () => clearInterval(eyeInterval);
    } else {
      setEyePosition({ x: 0, y: 0 });
    }
  }, [isScanning]);

  // Voice helper
  const speak = (text) => {
    const msg = new SpeechSynthesisUtterance(text);
    msg.rate = 1;
    msg.volume = 1;
    window.speechSynthesis.speak(msg);
  };

  const startScan = async () => {
    setIsScanning(true);
    setRecognitionStatus("scanning");
    setDetectedUser("");
    setEmotion("");

    // 1️⃣ Speak immediately on click
    speak("Starting analyzing, please look at the camera.");

    try {
      // 2️⃣ Call backend
      const res = await fetch("http://127.0.0.1:8000/recognize");
      const data = await res.json();

      if (!data || !data.user) {
        setRecognitionStatus("error");
        setIsScanning(false);
        speak("Error in recognition. Please try again.");
        return;
      }

      // 3️⃣ Update UI
      setRecognitionStatus("analyzing");
      await new Promise((resolve) => setTimeout(resolve, 1500));

      setRecognitionStatus("recognized");
      setDetectedUser(data.user);
      setEmotion(data.emotion);
      setIsScanning(false);

      // 4️⃣ Speak result
      if (data.user === "Unknown") {
        speak(`Unknown person detected. They look ${data.emotion}.`);
      } else if (data.user === "No face detected") {
        speak(`No face detected. Please look directly at the camera.`);
      } else {
        speak(`Hello ${data.user}, you look ${data.emotion} today.`);
      }

      // Reset status after 7 sec
      setTimeout(() => setRecognitionStatus("idle"), 7000);
    } catch (error) {
      console.error(error);
      setRecognitionStatus("error");
      setIsScanning(false);
      speak("Error connecting to backend.");
    }
  };

  const stopScan = () => {
    setIsScanning(false);
    setRecognitionStatus("idle");
    setDetectedUser("");
    setEmotion("");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex flex-col items-center justify-center p-8">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-white mb-2">Face Recognition System</h1>
        <p className="text-purple-300">AI-Powered Face & Emotion Detection</p>
      </div>

      {/* Robot Animation */}
      <div className="relative mb-8">
        {isScanning && (
          <div className="absolute inset-0 animate-ping">
            <div className="w-80 h-80 rounded-full border-4 border-cyan-400 opacity-20"></div>
          </div>
        )}

        {/* Robot Head */}
        <div className="relative w-80 h-80 bg-gradient-to-br from-slate-800 to-slate-700 rounded-3xl shadow-2xl flex items-center justify-center border-4 border-slate-600">
          {/* Antenna */}
          <div className="absolute -top-12 left-1/2 transform -translate-x-1/2 flex flex-col items-center">
            <div className="w-2 h-8 bg-slate-600 rounded-full"></div>
            <div className={`w-4 h-4 rounded-full ${isScanning ? "bg-cyan-400 animate-pulse" : "bg-slate-500"}`}></div>
          </div>

          {/* Face */}
          <div className="relative">
            {/* Eyes */}
            <div className="flex gap-12 mb-8">
              {[...Array(2)].map((_, i) => (
                <div
                  key={i}
                  className="relative w-20 h-24 bg-slate-900 rounded-2xl overflow-hidden border-2 border-slate-600"
                >
                  <div
                    className={`absolute top-1/2 left-1/2 w-12 h-12 rounded-full transition-all duration-100 ${
                      isScanning
                        ? "bg-cyan-400 shadow-lg shadow-cyan-400/50"
                        : "bg-purple-500"
                    }`}
                    style={{
                      transform: `translate(calc(-50% + ${eyePosition.x}px), calc(-50% + ${eyePosition.y}px))`,
                    }}
                  >
                    <div className="absolute top-2 left-2 w-4 h-4 bg-white rounded-full"></div>
                  </div>
                </div>
              ))}
            </div>

            {/* Mouth Display */}
            <div className="w-40 h-12 bg-slate-900 rounded-xl border-2 border-slate-600 flex items-center justify-center overflow-hidden">
              {recognitionStatus === "idle" && (
                <div className="w-24 h-1 bg-purple-500 rounded-full"></div>
              )}
              {recognitionStatus === "scanning" && (
                <div className="flex gap-2">
                  {[...Array(5)].map((_, i) => (
                    <div
                      key={i}
                      className="w-2 h-6 bg-cyan-400 rounded-full animate-pulse"
                      style={{ animationDelay: `${i * 0.1}s` }}
                    ></div>
                  ))}
                </div>
              )}
              {recognitionStatus === "analyzing" && (
                <Activity className="w-6 h-6 text-yellow-400 animate-spin" />
              )}
              {recognitionStatus === "recognized" && (
                <div className="w-20 h-8 border-4 border-green-400 rounded-full border-t-transparent animate-spin"></div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Recognition Result (Status Box Removed ✅) */}
      {detectedUser && (
        <div className="bg-green-900/30 border border-green-500 rounded-lg p-4 w-80 text-center mb-4">
          <User className="w-5 h-5 text-green-400 inline-block mb-1" />
          <p className="text-sm text-green-300">Recognized User</p>
          <p className="text-white font-semibold">{detectedUser}</p>
          <p className="text-green-400 text-sm mt-1">Emotion: {emotion}</p>
        </div>
      )}

      {/* Buttons */}
      <div className="flex gap-4">
        <button
          onClick={startScan}
          disabled={isScanning}
          className={`flex items-center gap-2 px-8 py-3 rounded-xl font-semibold transition-all ${
            isScanning
              ? "bg-slate-700 text-slate-500 cursor-not-allowed"
              : "bg-gradient-to-r from-cyan-500 to-blue-500 text-white hover:shadow-lg hover:shadow-cyan-500/50 hover:scale-105"
          }`}
        >
          <Camera className="w-5 h-5" />
          Start Recognition
        </button>

        <button
          onClick={stopScan}
          disabled={!isScanning}
          className={`flex items-center gap-2 px-8 py-3 rounded-xl font-semibold transition-all ${
            !isScanning
              ? "bg-slate-700 text-slate-500 cursor-not-allowed"
              : "bg-gradient-to-r from-red-500 to-pink-500 text-white hover:shadow-lg hover:shadow-red-500/50 hover:scale-105"
          }`}
        >
          Stop
        </button>
      </div>

      <div className="mt-8 text-center text-slate-400 text-sm">
        <p>Click "Start Recognition" to begin facial analysis</p>
      </div>
    </div>
  );
}
