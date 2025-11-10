import React, { useState, useEffect } from 'react';
import { Camera, User, Activity } from 'lucide-react';

export default function FaceRecognitionRobot() {
  const [isScanning, setIsScanning] = useState(false);
  const [recognitionStatus, setRecognitionStatus] = useState('idle');
  const [eyePosition, setEyePosition] = useState({ x: 0, y: 0 });
  const [detectedUser, setDetectedUser] = useState('');

  // 👁️ Eye animation
  useEffect(() => {
    if (isScanning) {
      const eyeInterval = setInterval(() => {
        setEyePosition({
          x: Math.sin(Date.now() / 200) * 8,
          y: Math.cos(Date.now() / 300) * 5
        });
      }, 50);
      return () => clearInterval(eyeInterval);
    } else {
      setEyePosition({ x: 0, y: 0 });
    }
  }, [isScanning]);

  // 🔊 Speak function
  const speak = (text) => {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "en-US";
    utterance.pitch = 1;
    utterance.rate = 0.95;
    utterance.volume = 1;
    window.speechSynthesis.cancel(); // stop previous voice
    window.speechSynthesis.speak(utterance);
  };

  // 🤖 Start Scan + Backend Integration
  const startScan = async () => {
    setIsScanning(true);
    setRecognitionStatus('scanning');
    setDetectedUser('');
    speak("Initiating facial scan. Please stay still.");

    setTimeout(async () => {
      setRecognitionStatus('analyzing');
      speak("Analyzing facial data...");

      try {
        const response = await fetch("http://127.0.0.1:8000/recognize");
        const data = await response.json();
        setRecognitionStatus('recognized');
        setDetectedUser(`${data.user} - ${data.emotion}`);

        // 🗣️ Voice Output
        speak(`User recognized. ${data.user}. Emotion detected: ${data.emotion}.`);
      } catch (error) {
        console.error("Backend connection failed:", error);
        setRecognitionStatus('error');
        speak("Error connecting to backend server.");
      }

      setIsScanning(false);
    }, 2000);
  };

  const stopScan = () => {
    setIsScanning(false);
    setRecognitionStatus('idle');
    setDetectedUser('');
    speak("Scanning stopped.");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex flex-col items-center justify-center p-8">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-white mb-2">Talking Face Recognition Robot 🤖</h1>
        <p className="text-purple-300">AI-powered identity verification with voice feedback</p>
      </div>

      {/* Robot Container */}
      <div className="relative mb-8">
        {isScanning && (
          <div className="absolute inset-0 animate-ping">
            <div className="w-80 h-80 rounded-full border-4 border-cyan-400 opacity-20"></div>
          </div>
        )}

        <div className="relative w-80 h-80 bg-gradient-to-br from-slate-800 to-slate-700 rounded-3xl shadow-2xl flex items-center justify-center border-4 border-slate-600 transition-all duration-300">
          {/* Antenna */}
          <div className="absolute -top-12 left-1/2 transform -translate-x-1/2 flex flex-col items-center">
            <div className="w-2 h-8 bg-slate-600 rounded-full"></div>
            <div className={`w-4 h-4 rounded-full ${isScanning ? 'bg-cyan-400 animate-pulse' : 'bg-slate-500'}`}></div>
          </div>

          {/* Face */}
          <div className="relative">
            {/* Eyes */}
            <div className="flex gap-12 mb-8">
              {['left', 'right'].map((side, i) => (
                <div key={i} className="relative w-20 h-24 bg-slate-900 rounded-2xl overflow-hidden border-2 border-slate-600">
                  <div
                    className={`absolute top-1/2 left-1/2 w-12 h-12 rounded-full transition-all duration-100 ${
                      isScanning
                        ? 'bg-cyan-400 shadow-lg shadow-cyan-400/50'
                        : 'bg-purple-500'
                    }`}
                    style={{
                      transform: `translate(calc(-50% + ${eyePosition.x}px), calc(-50% + ${eyePosition.y}px))`
                    }}
                  >
                    <div className="absolute top-2 left-2 w-4 h-4 bg-white rounded-full"></div>
                  </div>
                </div>
              ))}
            </div>

            {/* Mouth / Display */}
            <div className="w-40 h-12 bg-slate-900 rounded-xl border-2 border-slate-600 flex items-center justify-center overflow-hidden">
              {recognitionStatus === 'idle' && (
                <div className="w-24 h-1 bg-purple-500 rounded-full"></div>
              )}
              {recognitionStatus === 'scanning' && (
                <div className="flex gap-2">
                  {[...Array(5)].map((_, i) => (
                    <div key={i} className="w-2 h-6 bg-cyan-400 rounded-full animate-pulse" style={{ animationDelay: `${i * 0.1}s` }}></div>
                  ))}
                </div>
              )}
              {recognitionStatus === 'analyzing' && (
                <Activity className="w-6 h-6 text-yellow-400 animate-spin" />
              )}
              {recognitionStatus === 'recognized' && (
                <div className="w-20 h-8 border-4 border-green-400 rounded-full border-t-transparent animate-spin"></div>
              )}
              {recognitionStatus === 'error' && (
                <p className="text-red-400 text-xs font-bold">Error!</p>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Status Display */}
      <div className="bg-slate-800 rounded-xl p-6 w-96 mb-6 border border-slate-700">
        <div className="flex items-center justify-between mb-4">
          <span className="text-slate-400">Status:</span>
          <span className={`font-semibold ${
            recognitionStatus === 'idle' ? 'text-slate-400' :
            recognitionStatus === 'scanning' ? 'text-cyan-400' :
            recognitionStatus === 'analyzing' ? 'text-yellow-400' :
            recognitionStatus === 'recognized' ? 'text-green-400' :
            'text-red-400'
          }`}>
            {recognitionStatus.toUpperCase()}
          </span>
        </div>

        {detectedUser && (
          <div className="flex items-center gap-3 bg-green-900/30 border border-green-500 rounded-lg p-3">
            <User className="w-5 h-5 text-green-400" />
            <div>
              <p className="text-xs text-green-300">Recognized User</p>
              <p className="text-white font-semibold">{detectedUser}</p>
            </div>
          </div>
        )}

        {!detectedUser && recognitionStatus !== 'idle' && (
          <div className="text-center text-slate-400 py-2">
            <p className="text-sm">Processing facial data...</p>
          </div>
        )}
      </div>

      {/* Control Buttons */}
      <div className="flex gap-4">
        <button
          onClick={startScan}
          disabled={isScanning}
          className={`flex items-center gap-2 px-8 py-3 rounded-xl font-semibold transition-all ${
            isScanning
              ? 'bg-slate-700 text-slate-500 cursor-not-allowed'
              : 'bg-gradient-to-r from-cyan-500 to-blue-500 text-white hover:shadow-lg hover:shadow-cyan-500/50 hover:scale-105'
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
              ? 'bg-slate-700 text-slate-500 cursor-not-allowed'
              : 'bg-gradient-to-r from-red-500 to-pink-500 text-white hover:shadow-lg hover:shadow-red-500/50 hover:scale-105'
          }`}
        >
          Stop Scanning
        </button>
      </div>

      {/* Footer */}
      <div className="mt-8 text-center text-slate-400 text-sm">
        <p>Click "Start Recognition" to begin facial analysis</p>
      </div>
    </div>
  );
}
