/**
 * Stories you listen to. Classic children's-book cadence.
 * Public-domain retellings + one original house story.
 * Not wildlife encounters. Not the Signal Library.
 */

export const STORIES = Object.freeze([
  {
    id: "house-that-listened",
    title: "The House That Listened",
    source: "A Listener story",
    rights: "original",
    pages: [
      "Once there was a house.",
      "It was not a loud house.",
      "It sat by the trees and the dark and the weather.",
      "At night the house did not talk.",
      "The house listened.",
      "It listened for small feet in the grass.",
      "It listened for wings.",
      "It listened for rain, when rain was really there.",
      "If it did not know the sound, it did not pretend.",
      "It kept the sound, the way you keep a pebble in your pocket.",
      "That is how a house becomes a home node.",
      "Rings go out from the porch.",
      "Someone, somewhere, is still listening.",
    ],
  },
  {
    id: "wind-and-sun",
    title: "The Wind and the Sun",
    source: "After Aesop",
    rights: "public-domain",
    pages: [
      "The Wind and the Sun once had a quarrel.",
      "Each said, I am stronger.",
      "They saw a traveler on the road, wearing a coat.",
      "Whoever can make him take off the coat is stronger, said they.",
      "The Wind blew and blew.",
      "The traveler held the coat tighter.",
      "Then the Sun shone, warm and quiet.",
      "The traveler unbuttoned the coat, and took it off, and sat in the light.",
      "The Sun had won, without a shout.",
      "Listening is like that.",
      "It does not push.",
      "It waits, and the world opens.",
    ],
  },
  {
    id: "ugly-duckling",
    title: "The Ugly Duckling",
    source: "After Hans Christian Andersen",
    rights: "public-domain",
    pages: [
      "In the reeds, a duckling came last of all.",
      "He was not like the others, and they said so.",
      "He swam away. The world was wide and unkind.",
      "Winter came. He hid in the cold.",
      "When spring returned he saw white birds on the water.",
      "I will go to them, he thought, even if they send me off.",
      "He bowed his head — and saw himself.",
      "He was a swan.",
      "He had been a swan the whole time.",
      "The story does not rush the name.",
      "UNKNOWN stays UNKNOWN, until the spring is real.",
    ],
  },
  {
    id: "elves-shoemaker",
    title: "The Elves and the Shoemaker",
    source: "After the Brothers Grimm",
    rights: "public-domain",
    pages: [
      "There was a shoemaker who had leather for one last pair.",
      "He cut the leather, and went to bed, and left the work on the bench.",
      "In the morning the shoes were finished, and they were perfect.",
      "He sold them, and bought leather for two pairs.",
      "Again he cut, and slept, and in the morning the work was done.",
      "One night he and his wife kept watch.",
      "Tiny elves came in, and sewed, and hammered, and did not ask for thanks.",
      "The wife made them little clothes.",
      "The elves put them on, and danced, and did not come back.",
      "The work stayed good, because the first help had been real.",
      "Keep the original on the bench.",
      "Do not invent helpers who were never there.",
    ],
  },
]);

export function storyById(id) {
  return STORIES.find((s) => s.id === id) || STORIES[0];
}

export function storyScript(story) {
  return story.pages.join(" ");
}
