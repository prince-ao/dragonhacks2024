const title = document.getElementById('title')
const btn = document.getElementById('done-btn')
const audio_text = document.getElementById('audio-text')

btn.addEventListener('click', async () => {
    console.log("here")

    const response = await fetch("/end-lecture", {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ lecture: audio_text.textContent })
    })

    console.log(response)

    const redirectUrl = response.url

    window.location.href = redirectUrl
})

function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }

async function main() {
    const result = await fetch("/lecture", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({id: getCookie('ml')})
    })

    const result_json = await result.json();

    title.textContent = result_json['title']
}

main()

