let audioRecorder;
let intervalHandle;
let audioText;

async function sendData(data) {
  try {

    const response = await fetch("/api/v1/handle-audio/stream", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ data }),
    });

    const text_response = await response.text();

    audioText = document.getElementById('audio-text');
    console.log(text_response)

    audioText.textContent = audioText.textContent + " " +  text_response
  } catch (err) {
    console.log(err);
  }
}

async function sendStop() {
  try {
    const response = await fetch("/api/v1/handler-audio/stop");
    const text_response = await response.text();

    console.log(text_response);
  } catch (e) {
    console.log(e);
  }
}

async function startRecording() {
  let stream;

  try {
    stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  } catch (err) {
    console.error("Error accessing the microphone:", err);
    if (
      err.name === "NotAllowedError" ||
      err.name === "PermissionDeniedError"
    ) {
      throw new Error("Microphone access was denied by the user.");
    } else {
      throw new Error("Failed to access the microphone: " + err.message);
    }
  }

  const audioTrack = stream.getAudioTracks()[0];

  const audioStream = new MediaStream([audioTrack]);

  audioRecorder = new MediaRecorder(audioStream);

  let audioChunks = [];

  audioRecorder.ondataavailable = async function (e) {
    audioChunks.push(e.data);
  };

  audioRecorder.onstop = async function () {
    const audioBlob = new Blob(audioChunks, { type: "audio/ogg" });

    const reader = new FileReader();

    reader.onload = function () {
      const base64data = reader.result.split(",")[1];

      console.log("sending", base64data);
      sendData(base64data);
    };

    reader.onerror = function (error) {
      console.error("FileReader error: ", error);
    };

    reader.readAsDataURL(audioBlob);

    audioChunks = [];
  };

  audioRecorder.onerror = function (e) {
    console.log(e);
  };

  intervalHandle = setInterval(() => {
    audioRecorder.stop();

    setTimeout(() => {
      audioRecorder.start();
    }, 0);
  }, 5 * 1e3);

  audioRecorder.start();
}

async function stopRecording() {
  if (audioRecorder && audioRecorder.state !== "inactive") {
    audioRecorder.stop();
  }

  clearInterval(intervalHandle);
}
