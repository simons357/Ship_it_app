export type ShipChoice = {
  id: string;
  label: string;
  hint: string;
};

/** Step 1 — Ship to? */
export const shipToOptions: ShipChoice[] = [
  {
    id: "email",
    label: "Email",
    hint: "Send it straight to an inbox",
  },
  {
    id: "myself",
    label: "Myself later",
    hint: "Park it where you’ll find it tonight",
  },
  {
    id: "drive",
    label: "Cloud drive",
    hint: "Drop it in Drive, Dropbox, or iCloud",
  },
  {
    id: "person",
    label: "A person",
    hint: "Client, partner, friend — someone specific",
  },
  {
    id: "team",
    label: "Team channel",
    hint: "Slack, Teams, or a shared space",
  },
];

/** Step 2 — What do you want to happen? */
export const shipActionOptions: ShipChoice[] = [
  {
    id: "send-file",
    label: "Send a file",
    hint: "Hand off the finished thing",
  },
  {
    id: "share-link",
    label: "Share a link",
    hint: "Point them at the right place",
  },
  {
    id: "deliver",
    label: "Deliver finished work",
    hint: "It’s done — get it off your plate",
  },
  {
    id: "save",
    label: "Save for later",
    hint: "Done for now, findable later",
  },
];

export const CUSTOM_ID = "custom";
