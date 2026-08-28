extends Control
## Kuroto Dojo — loads the shared storyboard JSON. Same four skills as dojo.html.
## Godot is the budget team engine. Do not rebuild the 12 chapters here.

@onready var coach: Label = $Coach
@onready var status: Label = $Status

var board: Dictionary = {}
var skill_i: int = 0
var hold_ms: float = 0.0
var wave_counts: int = 0
var last_twist_ms: int = 0
var palms: int = 0
var bowed_in: bool = false
var bowed_out: bool = false
var chosen: String = ""
var space_held: bool = false
var palm_flash: float = 0.0
var t_ms: float = 0.0

const SKILL_IDS := ["leopard", "tai_chi", "surroundings", "spar"]
const ROOM := ["broom", "ribbon", "sand", "empty"]
const RED := Color(0.89, 0.11, 0.14)
const PAPER := Color(0.957, 0.918, 0.839)
const GOLD := Color(0.831, 0.686, 0.216)
const TEAL := Color(0.165, 0.435, 0.478)
const INK := Color(0.07, 0.04, 0.04)


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


func _skills() -> Array:
	return board.get("dojo", {}).get("skills", [])


func _skill() -> Dictionary:
	var skills := _skills()
	if skills.is_empty():
		return {}
	return skills[skill_i]


func _show_skill(i: int) -> void:
	var skills: Array = _skills()
	if skills.is_empty():
		coach.text = "No skills in storyboard."
		return
	skill_i = wrapi(i, 0, skills.size())
	var s: Dictionary = skills[skill_i]
	hold_ms = 0.0
	wave_counts = 0
	palms = 0
	bowed_in = false
	bowed_out = false
	chosen = ""
	palm_flash = 0.0
	coach.text = "%s  %s\n%s\nmaps to Pen: %s" % [
		s.get("name", ""), s.get("name_en", ""), s.get("coach", ""), s.get("maps_to_pen", "")
	]
	status.text = "Skill %d / %d — 1–4 jump. Space=leopard. Q/E=twist. F=bow/root. Enter=palm. G=room. Exercise. Cartoon. Nobody is wasted." % [skill_i + 1, skills.size()]
	queue_redraw()


func _process(delta: float) -> void:
	t_ms += delta * 1000.0
	if palm_flash > 0.0:
		palm_flash = max(0.0, palm_flash - delta * 1000.0)
	var s := _skill()
	if s.is_empty():
		return
	if s.get("kind", "") == "hold" and space_held:
		hold_ms += delta * 1000.0
		var need: float = float(s.get("seconds", 20)) * 1000.0
		if hold_ms >= need:
			status.text = "Leopard rooted. That was exercise. Bow."
	queue_redraw()


func _on_pen(g: String) -> void:
	var s := _skill()
	if s.is_empty():
		return
	var kind: String = str(s.get("kind", ""))
	if kind == "choose" and g == "twist":
		var idx := ROOM.find(chosen)
		chosen = ROOM[(idx + 1) % ROOM.size()]
		status.text = "Around you: %s. No mall sword." % chosen
	elif kind == "spar" and g == "squeeze":
		var n: int = int(s.get("exchanges", 3))
		if not bowed_in:
			bowed_in = true
			status.text = "Bow. Now three palms — Enter, not a flurry."
		elif palms >= n and not bowed_out:
			bowed_out = true
			status.text = "Bow after. Cartoon. Nobody is wasted."
		else:
			status.text = "Palms are Enter. F is the bow."
	elif kind == "spar" and g == "click":
		var n: int = int(s.get("exchanges", 3))
		if not bowed_in:
			status.text = "Bow first. F is the bow."
		elif palms >= n:
			status.text = "Three already. F to bow after."
		else:
			palms += 1
			palm_flash = 280.0
			status.text = "Palm %d / %d. Cartoon." % [palms, n]
	elif kind == "hold" and g == "squeeze":
		hold_ms += 2000.0
		status.text = "Rooted a little more. Squeeze is the stance."
	elif kind == "slow_sequence" and g == "twist":
		var now := Time.get_ticks_msec()
		if last_twist_ms != 0 and now - last_twist_ms < 500:
			status.text = "Too fast. Tai chi is not a punch."
			last_twist_ms = now
			return
		last_twist_ms = now
		var need: int = int(s.get("counts", 8))
		if wave_counts < need:
			wave_counts += 1
		status.text = "Wave count from the hand. Slow. %d / %d" % [wave_counts, need]
		if wave_counts >= need:
			status.text = "Tai chi wave complete. Slow on purpose."
	queue_redraw()


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		match event.keycode:
			KEY_1: _show_skill(0)
			KEY_2: _show_skill(1)
			KEY_3: _show_skill(2)
			KEY_4: _show_skill(3)
			KEY_RIGHT: _show_skill(skill_i + 1)
			KEY_LEFT: _show_skill(skill_i - 1)
			KEY_Q, KEY_E: _on_pen("twist")
			KEY_ENTER, KEY_KP_ENTER: _on_pen("click")
			KEY_F: _on_pen("squeeze")
			KEY_G:
				_show_skill(2)
				_on_pen("twist")
			KEY_SPACE:
				space_held = true
				_on_pen("squeeze")
	if event is InputEventKey and not event.pressed and event.keycode == KEY_SPACE:
		space_held = false


func _draw() -> void:
	var s := _skill()
	var floor_y := size.y - 80.0
	draw_rect(Rect2(0, floor_y, size.x, 80), Color(0.1, 0.06, 0.06))
	draw_line(Vector2(0, floor_y), Vector2(size.x, floor_y), GOLD, 2.0)
	for i in 14:
		var y := fmod(t_ms / 10.0, 18.0) + i * 22.0
		draw_line(Vector2(0, y), Vector2(size.x, y + 12), Color(0.89, 0.11, 0.14, 0.18), 2.0)
	var pose := "empty"
	if str(s.get("id", "")) == "leopard":
		pose = "leopard"
	elif str(s.get("id", "")) == "tai_chi":
		pose = "wave"
	elif str(s.get("id", "")) == "surroundings":
		pose = chosen if chosen != "" else "empty"
	elif str(s.get("id", "")) == "spar":
		if not bowed_in or (palms >= 3 and not bowed_out):
			pose = "bow"
		elif palm_flash > 0.0:
			pose = "palm"
	_draw_jun(Vector2(360, floor_y), pose)
	_draw_partner(Vector2(820, floor_y), pose == "bow")
	var title: String = str(s.get("name", "道場"))
	draw_string(ThemeDB.fallback_font, Vector2(40, 64), title, HORIZONTAL_ALIGNMENT_LEFT, -1, 28, RED)
	draw_string(ThemeDB.fallback_font, Vector2(40, 92), "SPEED RACER CEL · storyboard JSON · no sword tray", HORIZONTAL_ALIGNMENT_LEFT, -1, 16, GOLD)


func _draw_jun(feet: Vector2, pose: String) -> void:
	var squat := 18.0 if pose == "leopard" else 8.0
	var hip := feet + Vector2(0, -52 + squat)
	var head := hip + Vector2(0, -58)
	draw_circle(head, 16, PAPER)
	draw_rect(Rect2(hip.x - 16, hip.y - 28, 32, 42), PAPER)
	draw_line(hip + Vector2(-8, 8), feet + Vector2(-36 if pose == "leopard" else -20, 0), INK, 7.0)
	draw_line(hip + Vector2(8, 8), feet + Vector2(40 if pose == "leopard" else 22, 0), INK, 7.0)
	var lhand := hip + Vector2(-42, -10)
	var rhand := hip + Vector2(46, -18)
	if pose == "leopard":
		lhand = hip + Vector2(-70, -6)
		rhand = hip + Vector2(38, 8)
	elif pose == "wave":
		var a := (wave_counts + t_ms / 3000.0) * 0.7
		lhand = hip + Vector2(-36 + cos(a) * 28.0, -36 + sin(a) * 18.0)
		rhand = hip + Vector2(40 + cos(a + 1.2) * 26.0, -28 + sin(a + 1.2) * 16.0)
	elif pose == "bow":
		lhand = hip + Vector2(-10, 28)
		rhand = hip + Vector2(12, 28)
	elif pose == "palm":
		rhand = hip + Vector2(78, -36)
	elif pose == "broom" or pose == "ribbon":
		rhand = hip + Vector2(54, -48)
	draw_line(hip + Vector2(-12, -18), lhand, PAPER, 6.0)
	draw_line(hip + Vector2(12, -18), rhand, PAPER, 6.0)
	draw_circle(lhand, 7, GOLD)
	draw_circle(rhand, 7, GOLD)
	if pose == "broom":
		draw_line(rhand, rhand + Vector2(12, -90), Color(0.42, 0.29, 0.16), 4.0)
		draw_circle(rhand + Vector2(20, -96), 14, TEAL)
	elif pose == "ribbon":
		draw_line(rhand, rhand + Vector2(8, -88), RED, 4.0)
	elif pose == "sand":
		draw_colored_polygon(PackedVector2Array([
			feet + Vector2(-20, 0), feet + Vector2(0, -22), feet + Vector2(20, 0)
		]), GOLD)


func _draw_partner(feet: Vector2, bowing: bool) -> void:
	var hip := feet + Vector2(0, -48 + (10 if bowing else 0))
	var head := hip + Vector2(0, -50 + (18 if bowing else 0))
	draw_rect(Rect2(hip.x - 18, hip.y - 4, 36, 28), INK)
	draw_rect(Rect2(hip.x - 16, hip.y - 36, 32, 34), PAPER)
	draw_circle(head, 14, PAPER)
	draw_line(hip + Vector2(-10, 0), feet + Vector2(-22, 0), INK, 7.0)
	draw_line(hip + Vector2(10, 0), feet + Vector2(24, 0), INK, 7.0)
