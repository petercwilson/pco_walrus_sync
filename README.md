# 🎹 Planning Center → Walrus Clock Sync (Ruby)

Automatically sync your **Planning Center Services** setlists to a **Walrus Audio Clock MIDI pedal**.

This tool pulls your Celebration Service plans from Planning Center, extracts song metadata, and builds a MIDI setlist you can use to automate your Walrus Clock workflow.

---

## ✨ Features

* ✅ Locks to **Celebration Service** service type
* 🎯 Two operating modes:

  * **Auto mode** – finds the *next upcoming plan where you are scheduled*
  * 📅 **Manual mode** – pick *any Sunday by date*, even if you’re not scheduled
* 📜 Pulls song metadata:

  * Title
  * BPM
  * Time signature (meter)
  * Key
* 🎹 Generates a **MIDI file** compatible with Walrus Clock Program Change mapping
* 🔄 Handles **API pagination**, so any Sunday works (past or future)

---

## 🧰 Requirements

* **Ruby 3.x** ([https://rubyinstaller.org](https://rubyinstaller.org) for Windows)
* Internet access to Planning Center
* Planning Center **Personal Access Token**

### Required gems

```bash
gem install rest-client json midi-file
```

---

## 🔐 Planning Center Setup

1. Log into Planning Center

2. Go to **Developers → Personal Access Tokens**

3. Create a new token

4. Copy:

   * **Application ID**
   * **Secret**

5. Find your **Person ID**:

   * Go to People → your profile
   * Copy the number from the URL
   * Example: `/people/123456789` → `123456789`

---

## ⚙️ Configuration

Open `pco_walrus_sync.rb` and update:

```ruby
PC_APP_ID = "YOUR_APP_ID"
PC_SECRET = "YOUR_SECRET"
PERSON_ID = "YOUR_PERSON_ID"
TARGET_SERVICE_TYPE_NAME = "Celebration Service"
```

⚠️ Never share your API secret publicly.

---

## ▶ Running the Program

From the project folder:

```bash
ruby pco_walrus_sync.rb
```

You will be prompted:

```
1 - Next plan I am scheduled for
2 - Pick a specific Sunday date
```

If you choose option 2, enter a date like:

```
2026-02-01
```

---

## 📄 Output

The program will:

* Print the selected plan
* Display the full setlist
* Create a MIDI file:

```
weekly_setlist_with_meta.mid
```

You can:

* Open it in a DAW
* Test with virtual MIDI devices
* Send it to the Walrus Clock via USB/MIDI

---

## 🎛 Walrus Clock Usage

Typical workflow:

1. Map **Program Change numbers** to songs on the Walrus Clock
2. Run this tool weekly
3. Load/send the generated MIDI file
4. Your Clock recalls songs in service order automatically

---

## 🧪 Testing Without Hardware

You can test using:

* **loopMIDI** (virtual MIDI ports)
* **MIDI-OX** (monitor MIDI data)
* Any DAW (Ableton, Reaper, FL Studio, Cakewalk)

This lets you fully validate the system without owning the pedal.

---

## 🚀 Future Upgrade Ideas

* Live MIDI streaming instead of file export
* Automatic tempo changes per song
* One‑click Windows executable
* Simple GUI
* CSV or PDF setlist export
* Multi‑service support

---

## 📜 License

Personal project – free to modify and expand.

---

## 🙌 Credits

Built to connect **Planning Center Services** with the **Walrus Audio Clock** for worship automation and streamlined Sunday workflows.
