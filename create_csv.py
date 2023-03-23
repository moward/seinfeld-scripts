import csv
import dataclasses
import sqlite3
from itertools import islice

conn = sqlite3.connect("seinfeld.db")
curr = conn.cursor()

@dataclasses.dataclass
class Utterance:
    id: int
    episode_id: int
    utterance_number: int
    speaker: str
    text: str

def adjacent_pairs(it):
    it = iter(it)
    a, b = next(it), next(it)
    while True:
        try:
            yield a, b
            a, b = b, next(it)
        except StopIteration:
            return

def get_utterances() -> list[Utterance]:
    for row in curr.execute("select * from utterance order by episode_id asc, utterance_number asc;"):
        id, episode_id, utterance_number, speaker, text = row
        yield Utterance(id, episode_id, utterance_number, speaker, text)


with open('seinfeld-lines.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write header
    writer.writerow(('input_templated','output_templated'))
    
    for prev, curr in adjacent_pairs(get_utterances()):
        if curr.speaker == "JERRY":
            writer.writerow((
                "Below is a script from the American animated sitcom Seinfeld. "
                f"Write a response that completes {curr.speaker}'s last line in the "
                f"conversation. \n\n{prev.speaker}: {prev.text}\n{curr.speaker}:",
                curr.text
            ))
