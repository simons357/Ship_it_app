extends Control
## Loads the shared storyboard. Keep this file boring. Art comes later.

@onready var coach: Label = $Coach
@onready var status: Label = $Status

var board: Dictionary = {}
var skill_i: int = 0

func _ready() -> void:
	board = _load_board()
	_show_skill(0)
	print("Kuroto Dojo — ", board.get("title", ""), " — ", board.get("engines", {}).get("budget_team", "godot4"))

func _load_board() -> Dictionary:
	var paths = ["res://data/storyboard.json", "res://storyboard.json"]
	for p in paths:
		if FileAccess.file_exists(p):
			var f := FileAccess.open(p, FileAccess.READ)
			var parsed = JSON.parse_string(f.get_as_text())
			if typeof(parsed) == TYPE_DICTIONARY:
				return parsed
	push_warning("storyboard.json missing — copy engine/storyboard.json to res://data/")
	return {"title": "黒塔と湖", "dojo": {"skills": []}}

func _show_skill(i: int) -> void:
	var skills: Array = board.get("dojo", {}).get("skills", [])
	if skills.is_empty():
		coach.text = "No skills in storyboard."
		return
	skill_i = wrapi(i, 0, skills.size())
	var s: Dictionary = skills[skill_i]
	coach.text = "%s  %s\n%s\nmaps to Pen: %s" % [
		s.get("name", ""), s.get("name_en", ""), s.get("coach", ""), s.get("maps_to_pen", "")
	]
	status.text = "Skill %d / %d — 1–4 to jump. This is exercise. Cartoon spar. Nobody is wasted." % [skill_i + 1, skills.size()]

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		match event.keycode:
			KEY_1: _show_skill(0)
			KEY_2: _show_skill(1)
			KEY_3: _show_skill(2)
			KEY_4: _show_skill(3)
			KEY_RIGHT: _show_skill(skill_i + 1)
			KEY_LEFT: _show_skill(skill_i - 1)
