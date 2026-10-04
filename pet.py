"""Pet logic module for the Tamagotchi game."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Optional


@dataclass
class NegativeEvent:
    """Represents a negative event that affects the pet's stats."""

    name: str
    hunger_delta: int
    energy_delta: int
    happiness_delta: int

    def apply(self, pet: "Pet") -> None:
        """Apply the event effects to the pet."""
        pet.hunger += self.hunger_delta
        pet.energy += self.energy_delta
        pet.happiness += self.happiness_delta
        pet._clamp_stats()


class EventManager:
    """Manages random negative events that occur over time."""

    def __init__(self) -> None:
        self._events = [
            NegativeEvent("Bored", 0, -8, -12),
            NegativeEvent("Cold", 0, -12, -5),
            NegativeEvent("Very Hungry", -12, 0, -5),
            NegativeEvent("Dirty", 0, -3, -10),
            NegativeEvent("Restless", 0, -8, -8),
            NegativeEvent("Unwell", -5, -8, -10),
            NegativeEvent("Lonely", 0, 0, -12),
            NegativeEvent("Exhausted", -3, -10, -3),
        ]

    def get_random_event(self) -> Optional[NegativeEvent]:
        """Return a random negative event or None based on probability."""
        if random.random() < 0.40:
            return random.choice(self._events)
        return None


class Pet:
    """Represents a Tamagotchi pet."""

    MAX_STAT = 100
    MIN_STAT = 0

    CRITICAL_THRESHOLD = 10
    VERY_LOW_THRESHOLD = 20
    LOW_THRESHOLD = 40
    GOOD_THRESHOLD = 60
    GREAT_THRESHOLD = 80

    def __init__(
        self,
        name: str = "Mimi",
        hunger: int = 70,
        energy: int = 70,
        happiness: int = 70,
    ) -> None:
        """Initialize a new pet."""
        self.name = name.strip() or "Mimi"
        self.hunger = hunger
        self.energy = energy
        self.happiness = happiness
        self.is_alive = True

        self._clamp_stats()
        self._check_life_status()

    def _clamp_stats(self) -> None:
        """Clamp all stats between 0 and 100."""
        self.hunger = max(self.MIN_STAT, min(self.MAX_STAT, self.hunger))
        self.energy = max(self.MIN_STAT, min(self.MAX_STAT, self.energy))
        self.happiness = max(self.MIN_STAT, min(self.MAX_STAT, self.happiness))

    def _check_life_status(self) -> None:
        """Check if any stat has reached 0 and mark pet as dead if so."""
        if (
            self.hunger <= self.MIN_STAT
            or self.energy <= self.MIN_STAT
            or self.happiness <= self.MIN_STAT
        ):
            self.is_alive = False

    def feed(self) -> None:
        """Feed the pet. Increases hunger, energy, and happiness."""
        if not self.is_alive:
            return

        self.hunger += 20
        self.energy += 5
        self.happiness += 5

        self._clamp_stats()
        self._check_life_status()

    def play(self) -> None:
        """Play with the pet. Increases happiness but costs energy and hunger."""
        if not self.is_alive:
            return

        self.happiness += 20
        self.energy -= 10
        self.hunger -= 5

        self._clamp_stats()
        self._check_life_status()

    def sleep(self) -> None:
        """Let the pet sleep."""
        if not self.is_alive:
            return

        self.energy += 25
        self.hunger -= 8
        self.happiness += 5

        self._clamp_stats()
        self._check_life_status()

    def get_state(self) -> str:
        """Get the pet's current state based on its stats."""
        h = self.hunger
        e = self.energy
        f = self.happiness

        if (
            h <= self.CRITICAL_THRESHOLD
            or e <= self.CRITICAL_THRESHOLD
            or f <= self.CRITICAL_THRESHOLD
        ):
            return "Critical"

        if (
            h <= self.VERY_LOW_THRESHOLD
            or e <= self.VERY_LOW_THRESHOLD
            or f <= self.VERY_LOW_THRESHOLD
        ):
            return "Very tired and sad"

        if h <= self.LOW_THRESHOLD or e <= self.LOW_THRESHOLD or f <= self.LOW_THRESHOLD:
            return "Tired"

        if h >= self.GREAT_THRESHOLD and e >= self.GREAT_THRESHOLD and f >= self.GREAT_THRESHOLD:
            return "Fantastic"

        if h >= self.GOOD_THRESHOLD and e >= self.GOOD_THRESHOLD and f >= self.GOOD_THRESHOLD:
            return "Good"

        return "Normal"

    def get_speech(self) -> str:
        """Get a random speech message based on the pet's current state."""
        state = self.get_state()

        critical_messages = [
            "Mmm... I feel really bad...",
            "Please... take care of me...",
            "I don't have any strength left...",
            "I'm fading away...",
            "I'm so scared...",
        ]
        very_low_messages = [
            "I'm so tired and sad...",
            "I need help...",
            "I'm really weak...",
            "I can't hold on much longer...",
            "Oh... I feel awful...",
        ]
        tired_messages = [
            "I'm a bit tired...",
            "I need some rest...",
            "A nap would be nice right now...",
            "I'm feeling sluggish...",
            "Phew... I'm really tired...",
        ]
        normal_messages = [
            "Hello... want to play with me?",
            "I feel like doing something...",
            "Mmmmmm...",
            "What should we do now?",
            "I'm just hanging out...",
        ]
        good_messages = [
            "I feel pretty good!",
            "I have lots of energy!",
            "I'm having a nice day!",
            "Let's play!",
            "I'm feeling happy!",
        ]
        fantastic_messages = [
            "Wheeeeee! I feel amazing!",
            "I'm so happy!",
            "Let's play right now!",
            "I feel full of energy!",
            "What a wonderful day!",
        ]

        if state == "Critical":
            return random.choice(critical_messages)
        if state == "Very tired and sad":
            return random.choice(very_low_messages)
        if state == "Tired":
            return random.choice(tired_messages)
        if state == "Normal":
            return random.choice(normal_messages)
        if state == "Good":
            return random.choice(good_messages)
        if state == "Fantastic":
            return random.choice(fantastic_messages)
        return random.choice(normal_messages)

    def pass_time(self, event: Optional[NegativeEvent] = None) -> bool:
        """Advance time by applying a possible negative event."""
        if not self.is_alive:
            return True

        if event is not None:
            event.apply(self)

        self._check_life_status()
        return not self.is_alive

    def get_stats(self) -> dict:
        """Get current pet statistics as a dictionary."""
        return {
            "name": self.name,
            "hunger": self.hunger,
            "energy": self.energy,
            "happiness": self.happiness,
            "is_alive": self.is_alive,
            "state": self.get_state(),
        }
