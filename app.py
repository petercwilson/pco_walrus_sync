import streamlit as st
from datetime import date
from pco import (
    get_service_type_id,
    find_next_scheduled_plan,
    find_plan_by_date,
    fetch_plan_songs_with_meta
)
from midi_export import create_midi_file

st.set_page_config(page_title="PCO → Walrus Clock", page_icon="🎹")

st.title("🎹 Planning Center → Walrus Clock Sync")

st.markdown("Generate Walrus Clock MIDI setlists from Planning Center.")

# ---------- Credentials ----------

with st.expander("🔐 Planning Center Credentials"):
    PC_APP_ID = st.text_input("Application ID", type="password")
    PC_SECRET = st.text_input("Secret", type="password")
    PERSON_ID = st.text_input("Your Person ID")

if not PC_APP_ID or not PC_SECRET:
    st.warning("Enter your Planning Center credentials to continue.")
    st.stop()

# ---------- Mode ----------

mode = st.radio("Select mode:", [
    "Next Celebration Service I am scheduled for",
    "Pick a Celebration Service Sunday"
])

target_date = None
if "Pick" in mode:
    d = st.date_input("Select Sunday", value=date.today())
    target_date = d.isoformat()

# ---------- Run ----------

if st.button("🚀 Generate Walrus MIDI"):

    with st.spinner("Connecting to Planning Center..."):
        svc_id = get_service_type_id(PC_APP_ID, PC_SECRET)

        if "Pick" in mode:
            plan_id = find_plan_by_date(PC_APP_ID, PC_SECRET, svc_id, target_date)
        else:
            plan_id = find_next_scheduled_plan(PC_APP_ID, PC_SECRET, svc_id, PERSON_ID)

        if not plan_id:
            st.error("No matching Celebration Service plan found.")
            st.stop()

        songs = fetch_plan_songs_with_meta(PC_APP_ID, PC_SECRET, svc_id, plan_id)

    st.success("Setlist loaded!")

    st.subheader("🎶 Setlist Preview")

    for i, s in enumerate(songs, 1):
        st.write(f"{i}. {s['title']} | BPM: {s['bpm']} | TS: {s['meter']} | Key: {s['key']}")

    midi_bytes = create_midi_file(songs)

    st.download_button(
        "⬇ Download Walrus MIDI File",
        midi_bytes,
        file_name="walrus_setlist.mid",
        mime="audio/midi"
    )
