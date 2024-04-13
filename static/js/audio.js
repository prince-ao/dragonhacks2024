let audioRecorder;
let intervalHandle;

async function sendData(data) {
  console.log(data)
  try {
    await fetch("/api/v1/handle-audio", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ data }),
    });
  } catch (err) {
    console.log(err);
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
  }, 15 * 1e3);

  audioRecorder.start();
}

async function stopRecording() {
  if (audioRecorder && audioRecorder.state !== "inactive") {
    audioRecorder.stop();
  }

  clearInterval(intervalHandle);
}
