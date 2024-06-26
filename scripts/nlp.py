import base64
import io
import json
from pydub import AudioSegment
import speech_recognition as sr
from decouple import config
from openai import OpenAI
from ast import literal_eval
import os

r = sr.Recognizer()
client = OpenAI(api_key=config("OPENAI_API_KEY"))

def convert_webm_to_wav(webm_data):
    audio = AudioSegment.from_file(io.BytesIO(webm_data), format="webm")
    wav_io = io.BytesIO()
    audio.export(wav_io, format="wav")
    wav_io.seek(0)
    return wav_io

def convert_ogg_to_wav(ogg_data):
    audio = AudioSegment.from_file(io.BytesIO(ogg_data), format="ogg")
    wav_io = io.BytesIO()
    audio.export(wav_io, format="wav")
    wav_io.seek(0)
    return wav_io

def process_audio(data):
    text = ""
    try:
        wav_audio = convert_ogg_to_wav(data)

        with sr.AudioFile(wav_audio) as source:
            audio = r.record(source)

            try:
                text = r.recognize_google(audio)
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)

    return text

def convert_audio_to_text(base64_audio):
    binary_data = base64.b64decode(base64_audio)
    result = process_audio(binary_data)

    return result


class Hear2Learn:
    def __init__(self) -> None:

        self.summary_instruction = """Task: Analyze the input text and identify different topics being discussed. For each topic generate a summary. Generate the summaries as bullet points for each topic. 
        Generate atleast 5 bullet points and atmax 20 bullet points for each topic summary. Provide the result in the following format: Topic\n - bullet point1\n -bullet point2\n
        """
        
        self.quiz_instruction = """Task: Generate a quiz with 10 to 15 questions on the topics provided. Generate the response in json format with {"question": quesiton1, "options": [option1, option2, option3, option4], "answer": "anser1"}"""
        self.flashcard_instruction = """Task: Generate 5 flashcards based on the summary provided. Generate the response as a list of json format with {"front": "front1", "back": "back1"}"""
        
    def generate_app_config(self, temperature=0.):
        config={
            "llm": {
                "provider": "huggingface",
                "config": {
                    "model": 'mistralai/Mixtral-8x7B-Instruct-v0.1',
                    'top_p': 0.95,
                    'temperature': temperature,
                }
            },
            "embedder": {
                "provider": "huggingface",
                "config": {
                    "model": 'sentence-transformers/all-mpnet-base-v2'
                }
            }
        }
        return config
        
    def summarize_text(self, text):
        prompt = f'{self.summary_instruction}\n + Text: {text}'
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        summaries = response.choices[0].message.content
        # summaries = self.format_summaries(summaries)
        
        return summaries
    
    def generate_flashcards(self, summary):
        prompt = f'{self.flashcard_instruction}\n + Summary: {summary}'

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        flashcards = response.choices[0].message.content

        return flashcards


    
    def generate_quiz(self, context):
        self.app.add(context)
        answer = self.app.chat(self.quiz_instruction)
        quiz = answer.split('Answer')[-1]
        self.app.delete_session_chat_history()
        quiz = self.format_quiz(quiz)
        return quiz
    
    def chat(self, prompt):
        answer = self.app.chat(prompt)
        response = answer.split('Answer')[-1]
        self.app.delete_session_chat_history()
        return response
        
    def format_summaries(self, summaries):
        summaries = summaries.strip(':\n')
        summaries_list = []
        for s in summaries.split('Topic: ')[1:]:
            topic_summs = s.split('\n')
            topic = topic_summs[0]
            points = topic_summs[1:]
            summaries_list.append({
                "topic": topic,
                "points": [point.strip('-').strip() for point in points if len(point) > 1]
            })
            
        return summaries_list
    
    def format_quiz(self, quiz):
        return literal_eval(quiz.strip(":\n").replace("\n", ""))

if __name__ == '__main__':
    h = Hear2Learn()

    result = h.summarize_text("""In the last section, we examined some early aspects of memory. In this section, what we’re going to do is discuss some factors that influence memory. So let’s do that by beginning with the concept on slide two, and that concept is overlearning. Basically in overlearning, the idea is that you continue to study something after you can recall it perfectly. So you study some particular topic whatever that topic is. When you can recall it perfectly, you continue to study it.
This is a classic way to help when one is taking comprehensive finals later in the semester. So when you study for exam one and after you really know it all, you continue to study it. That will make your comprehensive final easier.

The next factor that will influence memory relates to what we call organization. In general, if you can organize material, you can recall it better. There are lots of different types of organizational strategies and I’ve listed those on slide four. So let’s begin by talking about the first organizational strategy called clustering and is located on page five.

In clustering, basically you recall items better if you can recognize that there are two or more types of things in a particular list. So let’s give a couple of lists and show you some examples of that. These examples are shown in slide six.

Let’s say that I give you the first list; north, cardinal, south, robin, east, wren, west, sparrow. Now if you can recognize that north, south, east and west are points on a compass and cardinal, robin, wren and sparrow are birds, then you have a higher probability of recalling that material than if you just tried to recall the list in order.

The same occurs with the second list that is located on the right hand side of page six. So let’s list these words as well; pig, cat, horse, dog, sheep, birds, cow, and fish. Now if you can recognize that these are two groups of animals; one being farm animals and the other being domestic companions, ala, pets, then you can recall that list of material better than if you just tried to recall the list in order. So again, this is another type of example of organizational strategy.

Now there are other organizational strategies that one can use as well. The next one of these, as we see on slide seven, are what are called verbal pneumonic techniques. In verbal pneumonic techniques, you make your own organization and there are many, many different types of techniques. So let’s talk about the first of these on slide eight and that is called acrostics. In acrostics these are phrases in which the first letter of each word functions as a cue to help you recall some piece of information. There are a variety of different acrostics that one uses. The most famous of these relates to this saying: On Old Olympus Towering Tops A Fin And German Vented Some Hops. These relate to the twelve different cranial nerves that we have within the brain and if you are a traditional medical student or taking anatomy and physiology, this is the acrostic that you usually use to remember them.

Now there are other verbal pneumonic techniques as well. So let’s take a look at another one of those and is located in slide 10. These are called acronyms. Acronyms are basically a word formed out of the first letters of a series of words. A classic example of an acronym system is ROY G BIV which are the first letters of the colors in the visual spectrum. This is the classic acronym that all sensation and perception students and even introductory psych students learn to memorize. Another verbal pneumonic technique is shown on slide 11 and called Rhymes. The classic rhyme is one that you had learned in grade school is I before E except after C. So rhymes are another way to recall and memorize information.

So now we’ve examined a variety of different verbal pneumonic techniques and how they work. In this next section, we’re going to examine some visual imagery types of methods to organize material.

The first of these is shown in slide 13 and is called the Method of Loci. Basically it involves taking some kind of an imaginary walk along some familiar path where images that you’re trying to recall are associated with some items or locations along the path. The classic example of where we put material is in your house. So just close your eyes and think about this. What happens when you walk in your back door? What’s the first item that you see. Well the first item that you see is where you put the first piece of information that you want to remember. Let’s say that it is a coat hook, so you hang something on the coat hook. Then you continue on into the kitchen. In the kitchen, what’s the first thing that you see? Well it may be the refrigerator, and so you identify the second item that you’re trying to remember and put it on the refrigerator. Then you open the door in the refrigerator and that’s where you put your third item. And then you close the refrigerator door and you look to your left and there’s the stove. So, you put the next item on one of the burners of the stove and on and on until you have all the items that you are trying to remember located within the kitchen or within the house.

Then when you’re trying to recall the items during the exam, you begin your walk around the house. So the first thing you think about is what happens when I walk in the back door and lo and behold, there’s the first item I’m trying to recall. Then I go to the refrigerator and there’s the second item. Then I open the door of the refrigerator and there’s the third item and on and on until I have all the different materials that I’m trying to remember put down for my exam.

Now walking around the house is a good place to use the method of loci, but there are other places that’s even better. The better place to try and place all the information you want to learn is in the location where you’re going to have to recall the material. So sitting in the exam room where you’re going to take the test and putting all those things on different objects within the exam room is a good strategy. Especially if one is trying to memorize lots and lots of different information because each of those places acts as a cue.

So that’s the first type of visual imagery technique. Now the second type of visual imagery technique is shown on slide 14. This is called the pegword technique. The pegword technique relies on a list of integers. What you do is attach a pegword to each of the numbers with rhymes. The classic example is One rhyming with Bun, Two and Shoe, Three and Tree, Four and Door and on and on. Then as we see in slide 15, when you’re given a list of words to recall, you associate the first word in the list with the peg word. For example you have a word, let’s say you’re trying to recall the word “Bee” and the peg word is bun. Well what you might try to do is visualize a bee eating a great big bun. As a result of that, you make associations. Furthermore, the more outrageous the association, the better the recall is for the particular item. So, let’s say that you might have a frog with shoes on, and a horse knocking down a tree, or whatever it may be to the information that you’re trying to recall.

So these are the first two techniques (overlearning, organization) that relate to factors that influence memory. What’s the next major factor? Well, the next major factor is shown on slides 16 and 17 and that is the order in which you learn things. If I give you a list of words in a serial learning task or a free recall task, you have better recall for words at the beginning and end of a list but not in the middle of a particular list. That is called the Serial Position Effect. There’s a couple different things you need to note about the serial position effect. First recall at the beginning of the list is what is called the Primacy Effect and recall for the end of the list is called the Recency Effect. The recency effect occurs because you can generally only recall seven plus or minus two items in working or what is also called short term memory. We’ll talk about that in more detail a little bit later.

Now the serial position effect is shown in the graphical figure on slide 19. As we can see when we start to memorize a list of words, we usually start about 60 to 65% accuracy. In the recency phase, at the last word that we’re trying to recall we have a percent recall rate of about 85 to 90% depending on the study. Note within the middle of the list that you’re trying to look at you only have about a 20% chance of recalling a particular set of items.

So the serial recall effect is extremely important for how you try to memorize things. For example, if you were studying three chapters for learning, as what we might have here, and you always start with the first chapter in order (so you start with chapter one, then two, then three), you will have fairly good recall for chapter one, you’ll have some decent recall also for chapter three but chapter two you won’t remember at all. So a better way to memorize that material is to change the order in which you’re learning the material. So you start one day with chapters one, two, and three in that order, then you go with two, three, and one; and finally, three, one and two, and on and on. What this does is help you raise the level of the middle section within the recency of effect. So, within the serial learning effect, what you should do is vary the order so you have good recall of information.

Now there’s another variable that goes along with the serial position effect and is shown on slide 20. It is called the Von Resterhoff Effect. Basically when a word is in the middle of a list that is surprising or funny or dirty, you will usually recall that particular word and some of those around it. So let’s give an example of that in the following slide.

Look on slide 21 at the list of words. What I’d like you to do is try to recall the words in order. So, take a minute to do that.

Now that you have memorized and tried to recall the words, look in the middle of the list. Basically what happens is that everybody will recall the word “intercourse” and usually a couple of words around it. So you might recall elephant and even suitcase. This effect is shown on slide 22. So, we have the same kind of effect that we saw with the serial learning task we began with on earlier slides. But we also see that in the middle of the list, we recall one or two particular words, then we drop off again before we have a recency effect (starting toward words 14 and 15). So again, the Von Resterhoff effect is an extremely important effect. You can use it to your advantage by putting surprising or interesting things in the middle of the list of material that you’re trying to memorize.

Now the next factor that influences learning and memory is what we call proactive interference or what is also called proactive inhibition. Here is where your past learning will interfere with your ability to recall new material. Let’s give an example, if you learn list A, then you learn list B, and finally you have to recall B. In proactive interference, list A will interfere with your ability to recall list B. A classic example is shown on slide 24. You learn sociology then you learn psychology. Sociology will interfere with your ability to recall the psychology. To help keep it clear we have a little organizational scheme that kind of helps us. That is a classic acronym PABB. Proactive - You learn A, you learn B, then you recall B.

Now sometimes your past learning will interfere with information retention or sometimes your past learning will help you because you learn to organize it better. We will talk about this in more detail in the next section.

The next factor that influences memory is shown on slide 26 and that is what is called retroactive interference or retroactive inhibition. Unlike proactive interference, learning new material interferes with your ability to recall old material. That is, you learn list C, then you learn list D, then you have to recall C. Consequently, D will interfere with your ability to recall C.

So let’s take an example of that. Here you learn psychology, then you learn sociology, and sociology will interfere with your ability to recall the psychology. So let’s take another example and use a more practical example. Let’s say that you’re learning psychology, (ala learning) and you’re going to take a test. You walk into the exam and you have about five minutes before the exam starts. So you take out a newspaper such as the Argonaut, which is our school newspaper and you start to read it. Consequently, the Argonaut will interfere with your ability to recall the psychology. Again we have another acronym and that is RCDC. Retroactive - you learn C, you learn D, then you have to recall the C.

What are important things for you about proactive and retroactive interference from an applied standpoint. This is shown in slide 29. First of all, don’t take similar courses in the same semester. Take things that are different and that don’t have a lot of overlap. As a result you will recall all of them better. An example might be taking some sociology, some math, biology and computer science rather than taking sociology, psychology, anthropology, and maybe political science. If you do, things just get jumbled together.

Now the next variable that’s going to influence learning is what is called active participation. In general, the more active you are during the learning cycle, the more you will recall, This is shown in slide 31. Quizzing yourself while you’re reading, determining how the material that you’re currently working with relates to other material, using study guides, outlining the chapters or notes, etc., will significantly increase your recall of information.

The major one these relates to highlighting and chapter outlining or reading. If you look at and see which gives you the better recall, there is no doubt about it that outlining your book chapter will give you better recall than highlighting or reading the book. Let’s just take the concept of highlighting. What are you doing when you highlight a piece of text, let’s say a paragraph or two. What are you doing when you’re doing that? Essentially, what you’re trying to do is keep the yellow or pink line going over the text. You are not really using the information or putting it into your brain system. Whereas if you are outlining some book chapter or some notes, what are you having to do. First, you have to read it, then you have to put it into some kind of verbal vocabulary. Once you have the verbal vocabulary, you have to write it on paper and make sure that it makes sense as you’re doing that. So, when you outline a chapter, you’re putting information into your brain four or five different ways, rather than putting it in and using one or two ways, such as with highlighting or even reading.

Now the next variable that will impact learning is the similarity of the learning and recall condition. In general, the more similar the recall condition is to the learning condition, the better the recall. This is a classic example that is shown in slide 33. The ideal place to study for an exam is where, the room where you’re going to take the exam. Here you have all the cues. And the more similar it is, (everybody studying in the same room) the more information you recall.

Now there’s a related concept that goes with the similarity of learning and recall condition and this is shown in slide 35. It is called state dependent learning. What state dependent learning basically says is this. “It’s best to recall information in the same drug state as you are when you’re doing the learning.” So, as we see on slide 36, if you smoke, you need to smoke while taking your exam. If you drink coffee or coke while you’re studying, you need to drink coffee or coke while taking the exam.

When I was in grad school many, many years ago, I drank a lot of Coca Cola, but I knew exactly how my body felt when I was taking the exam and when I was drinking the Coke while studying. If my Coca Cola level was off, I did poorer on the exam.

Now a related variable is if you don’t study while drinking coffee, but take the exam on coffee, what happens? Well what happens is that you don’t recall as well (and the same is true with smoking). Since people aren’t allowed to smoke in auditoriums or wherever they are taking exams, it’s best not to smoke when you’re studying.

Now this concept relates to a concept that is called test anxiety and in test anxiety, what you’re doing is something very similar, and this is shown in slide 37. In test anxiety, basically while you’re studying you tend to be relaxed, but when you’re taking the exam, you tend to get tense due to the stress of the exam. When you’re tense, what happens? Your blood pressure goes up, different hormones are released, etc. As a result, your mind goes “poof” and everything’s gone. Then what happens when you get done with the exam. You walk out, you begin to relax, and guess what happens, you can recall the information again.

So, the best way to help yourself is to learn to stay relaxed while you’re taking your exam. If you have problems doing that, participate in a test anxiety workshop. There are a variety of those located at a variety of different settings. Furthermore, any good clinical or counseling psychologist can help you with that.

Now the next variable that relates to factors that influence learning and memory relates to spaced practice being better than massed practice (or what is called cramming). This is shown on slide 39. In general, it’s better to spread out studying over a period of time instead of doing it all at once. Let’s give an example of that on slide 40. Basically studying three days for one hour is better than studying three hours all at once. That is, don’t cram for the exam. The question then becomes why? As we show in slide 41, the reason you have problems is because of the serial position curve. Generally you can only recall seven plus or minus two items in your memory, so when you’re cramming, basically what you’re doing is putting in information into your short term memory. Thus what you have is recalling of recency effect items.

So in summary as we see here in the last few minutes is that there’s a variety of different factors that influence memory. Each of these factors is extremely important and ones that you should remember. In the next section, we’re going to begin to examine some early theories of memory and how those theories work.""")

    flashcards = h.generate_flashcards(result)

    print(flashcards)
