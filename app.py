"""Streamlit app for the Tamagotchi pet game."""

from __future__ import annotations

import time

import streamlit as st

from pet import EventManager, Pet


def initialize_session_state() -> None:
    """Initialize Streamlit session state variables."""
    if "pet" not in st.session_state:
        st.session_state.pet = Pet(name="Mimi")

    if "ticks" not in st.session_state:
        st.session_state.ticks = 0

    if "speech_interval" not in st.session_state:
        st.session_state.speech_interval = 2

    if "event_manager" not in st.session_state:
        st.session_state.event_manager = EventManager()

    if "last_speech_tick" not in st.session_state:
        st.session_state.last_speech_tick = 0

    if "show_speech" not in st.session_state:
        st.session_state.show_speech = True

    if "game_over" not in st.session_state:
        st.session_state.game_over = False

    if "speech_text" not in st.session_state:
        st.session_state.speech_text = st.session_state.pet.get_speech()


def reset_game() -> None:
    """Reset the game to initial state."""
    pet_name = st.session_state.pet.name if "pet" in st.session_state else "Mimi"

    st.session_state.pet = Pet(name=pet_name)
    st.session_state.ticks = 0
    st.session_state.last_speech_tick = 0
    st.session_state.game_over = False
    st.session_state.speech_text = st.session_state.pet.get_speech()
    st.rerun()


def apply_tick() -> None:
    """Advance time by one tick."""
    if st.session_state.game_over or not st.session_state.pet.is_alive:
        return

    pet = st.session_state.pet
    event_manager = st.session_state.event_manager

    st.session_state.ticks += 1
    current_tick = st.session_state.ticks

    event = event_manager.get_random_event()
    if event is not None:
        st.session_state.last_event = f"Oh no! {event.name} happened!"
        pet.pass_time(event)
    else:
        pet.pass_time(None)

    should_speak = (
        current_tick - st.session_state.last_speech_tick
    ) >= st.session_state.speech_interval

    if should_speak and pet.is_alive:
        st.session_state.speech_text = pet.get_speech()
        st.session_state.last_speech_tick = current_tick
        st.session_state.show_speech = True

    if not pet.is_alive:
        st.session_state.game_over = True


def handle_action(action: str) -> None:
    """Handle pet actions (feed, play, sleep)."""
    if st.session_state.game_over or not st.session_state.pet.is_alive:
        return

    pet = st.session_state.pet

    if action == "feed":
        pet.feed()
    elif action == "play":
        pet.play()
    elif action == "sleep":
        pet.sleep()

    time.sleep(0.05)
    apply_tick()
    st.rerun()


def render_pet_speech() -> None:
    """Render the pet's speech bubble."""
    if not st.session_state.show_speech or st.session_state.game_over:
        return

    pet = st.session_state.pet
    if not pet.is_alive:
        return

    speech = st.session_state.speech_text
    pet_name = pet.name

    st.markdown(
        f"""
        <div style="
            background-color: #f0f2f6;
            border-radius: 15px;
            padding: 1rem 1.25rem;
            margin: 0.5rem 0 1rem 0;
            border-left: 4px solid #4A90E2;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            position: relative;
        ">
            <strong>{pet_name}:</strong> {speech}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_stats() -> None:
    """Render pet statistics with progress bars."""
    pet = st.session_state.pet

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Hunger", f"{pet.hunger}/100")
        st.progress(pet.hunger / 100)

    with col2:
        st.metric("Energy", f"{pet.energy}/100")
        st.progress(pet.energy / 100)

    with col3:
        st.metric("Happiness", f"{pet.happiness}/100")
        st.progress(pet.happiness / 100)

    state = pet.get_state()
    st.markdown(f"**Status:** {state}")


def render_actions() -> None:
    """Render action buttons for the pet."""
    pet_alive = not st.session_state.game_over and st.session_state.pet.is_alive

    col1, col2, col3 = st.columns(3)

    with col1:
        st.button(
            "🍔 Feed",
            use_container_width=True,
            disabled=not pet_alive,
            on_click=handle_action,
            args=("feed",),
            type="primary",
        )

    with col2:
        st.button(
            "🎾 Play",
            use_container_width=True,
            disabled=not pet_alive,
            on_click=handle_action,
            args=("play",),
            type="primary",
        )

    with col3:
        st.button(
            "😴 Sleep",
            use_container_width=True,
            disabled=not pet_alive,
            on_click=handle_action,
            args=("sleep",),
            type="primary",
        )


def render_game_over() -> None:
    """Render game over screen."""
    if not st.session_state.game_over:
        return

    pet_name = st.session_state.pet.name
    ticks_survived = st.session_state.ticks

    st.error("**GAME OVER**", icon="💔")
    st.markdown(f"**{pet_name} has escaped!**")
    st.markdown("You didn't take care of them well enough...")
    st.markdown(f"**Ticks survived:** {ticks_survived}")
    st.markdown("---")
    st.button("🔄 Try Again", on_click=reset_game, type="primary", use_container_width=True)


def render_event_notification() -> None:
    """Render notification for negative events."""
    if "last_event" not in st.session_state:
        return
    if st.session_state.game_over:
        return

    st.warning(st.session_state.last_event, icon="⚠️")
    del st.session_state.last_event


def main() -> None:
    """Main Streamlit application entry point."""
    st.set_page_config(
        page_title="Tamagotchi Pet",
        page_icon="🐾",
        layout="centered",
        initial_sidebar_state="collapsed",
    )

    initialize_session_state()

    st.title("🐾 Tamagotchi Pet")
    st.markdown("Take care of your pet, or it will escape!")

    render_event_notification()

    if st.session_state.game_over:
        render_game_over()
        return

    pet = st.session_state.pet
    new_name = st.text_input(
        "Pet name",
        value=pet.name,
        max_chars=20,
        placeholder="Enter pet name...",
        help="Rename your pet",
    )

    if new_name != pet.name:
        pet.name = new_name.strip() or "Mimi"
        st.session_state.speech_text = pet.get_speech()

    render_pet_speech()
    render_stats()

    st.markdown("---")
    render_actions()

    with st.expander("Game Info", expanded=False):
        st.markdown(
            """
            **Rules:**
            - Feed: +Hunger (+20), +Energy (+5), +Happiness (+5)
            - Play: +Happiness (+20), -Energy (-10), -Hunger (-5)
            - Sleep: +Energy (+25), +Happiness (+5), -Hunger (-8)

            **Game Over:** If any stat reaches 0, your pet escapes and you lose.

            **Time:** Negative events can happen (40% chance per action).
            Your pet speaks periodically based on its current mood and state.
            """
        )
        st.metric("Ticks Survived", st.session_state.ticks)


if __name__ == "__main__":
    main()
