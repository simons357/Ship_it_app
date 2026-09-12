/**
 * Lessons in listening. For a real person to teach.
 * Do not invent a named expert. The older and rarer the listening, the better.
 * Not wildlife encounters. Not the Signal Library.
 */

import { dayNumber } from "./stories.js";

export const LESSONS = Object.freeze([
  {
    id: "older-kind",
    title: "An Older Kind of Listening",
    source: "For whoever is teaching",
    rights: "original",
    rare: true,
    pages: [
      "Someone can teach listening.",
      "Not a host. Not a show.",
      "A person who still knows how to sit still.",
      "The older the listening, the better.",
      "The rarer the listening, the better.",
      "You do not need a new name for the sound.",
      "You need time, and a quiet place, and one true ear.",
      "That is the lesson. Now you try.",
    ],
  },
  {
    id: "without-a-name",
    title: "When You Do Not Know the Sound",
    source: "For whoever is teaching",
    rights: "original",
    rare: true,
    pages: [
      "A sound comes.",
      "You do not know its name.",
      "The old way is not to guess.",
      "Keep the sound. Leave it UNKNOWN.",
      "UNKNOWN is not empty. It is honest.",
      "Later, if the name is real, it can come.",
      "Tonight, not knowing is allowed.",
    ],
  },
  {
    id: "how-a-story",
    title: "How a Story Wants to Be Heard",
    source: "For whoever is teaching",
    rights: "original",
    rare: true,
    pages: [
      "A story is older than a screen.",
      "Someone tells it. Someone listens.",
      "Do not rush the page.",
      "Do not explain every word.",
      "Let the quiet sit between the lines.",
      "That quiet is part of the story.",
      "When it is done, say good night, and stop.",
    ],
  },
  {
    id: "the-field",
    title: "Listening to the Field",
    source: "For whoever is teaching",
    rights: "original",
    rare: true,
    pages: [
      "The field is not a playlist.",
      "It is weather, and wings, and what lives that is not us.",
      "Put the phone down.",
      "If rain is there, listen to rain.",
      "If rain is not there, do not invent it.",
      "Rings go out from the porch.",
      "That is field listening. It is old. It is enough.",
    ],
  },
  {
    id: "night-ear",
    title: "Listening at Night",
    source: "For whoever is teaching",
    rights: "original",
    rare: true,
    pages: [
      "Night is a good teacher, if you let it be.",
      "The house gets quieter.",
      "Small sounds get larger.",
      "You do not have to name them.",
      "You only have to stay.",
      "Then sleep. The night will go on listening.",
    ],
  },
  {
    id: "rare-ear",
    title: "A Rarer Ear",
    source: "For whoever is teaching",
    rights: "original",
    rare: true,
    pages: [
      "Most people listen for what they already know.",
      "A rarer ear waits for what it has not heard yet.",
      "That takes longer.",
      "It does not win a prize.",
      "It keeps the original, the way you keep a pebble.",
      "If you can teach that, teach that.",
    ],
  },
  {
    id: "do-not-push",
    title: "Listening Does Not Push",
    source: "For whoever is teaching",
    rights: "original",
    rare: true,
    pages: [
      "The Wind pushed, and the coat stayed on.",
      "The Sun waited, and the coat came off.",
      "Listening is the Sun’s work.",
      "It does not shout the animal’s name.",
      "It does not fill the quiet with a guess.",
      "It waits, and the world opens, or it does not.",
      "Both answers are true enough for tonight.",
    ],
  },
]);

export function lessonById(id) {
  return LESSONS.find((s) => s.id === id) || LESSONS[0];
}

/** One listening lesson a day. Same calendar day, same lesson. */
export function todayLesson(date = new Date()) {
  const rare = LESSONS.filter((s) => s.rare);
  const pool = rare.length ? rare : LESSONS;
  return pool[Math.abs(dayNumber(date)) % pool.length];
}
