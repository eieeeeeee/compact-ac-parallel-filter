#!/usr/bin/env python3
import json, sys
from pathlib import Path

p = Path(sys.argv[1])
j = json.loads(p.read_text(encoding="utf-8"))

rule_severities = {
  "annular_width":"error","clearance":"error","connection_width":"warning",
  "copper_edge_clearance":"error","copper_sliver":"warning","courtyards_overlap":"error",
  "creepage":"error","diff_pair_gap_out_of_range":"error",
  "diff_pair_uncoupled_length_too_long":"error","drill_out_of_range":"error",
  "duplicate_footprints":"warning","extra_footprint":"warning","footprint":"error",
  "footprint_filters_mismatch":"ignore","footprint_symbol_field_mismatch":"warning",
  "footprint_symbol_mismatch":"warning","footprint_type_mismatch":"ignore",
  "hole_clearance":"error","hole_to_hole":"warning","holes_co_located":"warning",
  "invalid_outline":"error","isolated_copper":"warning","item_on_disabled_layer":"error",
  "items_not_allowed":"error","length_out_of_range":"error","lib_footprint_issues":"warning",
  "lib_footprint_mismatch":"warning","malformed_courtyard":"error","microvia_drill_out_of_range":"error",
  "mirrored_text_on_front_layer":"warning","missing_courtyard":"ignore","missing_footprint":"warning",
  "missing_tuning_profile":"warning","net_conflict":"warning","nonmirrored_text_on_back_layer":"warning",
  "npth_inside_courtyard":"error","padstack":"warning","pth_inside_courtyard":"error",
  "shorting_items":"error","silk_edge_clearance":"warning","silk_over_copper":"warning",
  "silk_overlap":"warning","skew_out_of_range":"error","solder_mask_bridge":"error",
  "starved_thermal":"error","text_height":"warning","text_on_edge_cuts":"error",
  "text_thickness":"warning","through_hole_pad_without_hole":"error","too_many_vias":"error",
  "track_angle":"error","track_dangling":"warning","track_not_centered_on_via":"ignore",
  "track_on_post_machined_layer":"error","track_segment_length":"error","track_width":"error",
  "tracks_crossing":"error","tuning_profile_track_geometries":"ignore","unconnected_items":"error",
  "unresolved_variable":"error","via_dangling":"warning","zones_intersect":"error"
}

j["board"] = {
  "3dviewports": [],
  "design_settings": {
    "defaults": {
      "apply_defaults_to_fp_barcodes":False,"apply_defaults_to_fp_dimensions":False,
      "apply_defaults_to_fp_fields":False,"apply_defaults_to_fp_shapes":False,
      "apply_defaults_to_fp_text":False,"board_outline_line_width":0.05,
      "copper_line_width":0.2,"copper_text_italic":False,"copper_text_size_h":1.5,
      "copper_text_size_v":1.5,"copper_text_thickness":0.3,"copper_text_upright":False,
      "courtyard_line_width":0.05,"dimension_precision":4,"dimension_units":3,
      "fab_line_width":0.1,"fab_text_italic":False,"fab_text_size_h":1.0,
      "fab_text_size_v":1.0,"fab_text_thickness":0.15,"fab_text_upright":False,
      "other_line_width":0.1,"other_text_italic":False,"other_text_size_h":1.0,
      "other_text_size_v":1.0,"other_text_thickness":0.15,"other_text_upright":False,
      "pads":{"drill":0.8,"height":1.27,"width":1.27},
      "silk_line_width":0.1,"silk_text_italic":False,"silk_text_size_h":1.0,
      "silk_text_size_v":1.0,"silk_text_thickness":0.1,"silk_text_upright":False,
      "zones":{"border_display_style":2,"border_hatch_pitch":0.5,"corner_radius":0.0,
        "corner_smoothing":0,"fill_mode":0,"hatch_gap":1.5,"hatch_orientation":0.0,
        "hatch_smoothing_level":0,"hatch_smoothing_value":0.1,"hatch_thickness":1.0,
        "min_clearance":0.5,"min_island_area":10.0,"min_thickness":0.25,
        "pad_connection":1,"remove_islands":0,"thermal_relief_gap":0.5,
        "thermal_relief_spoke_width":0.5}
    },
    "diff_pair_dimensions": [],
    "drc_exclusions": [],
    "meta":{"version":2},
    "rule_severities": rule_severities,
    "rules":{
      "max_error":0.005,"min_clearance":0.1,"min_connection":0.0,
      "min_copper_edge_clearance":0.5,"min_groove_width":0.0,
      "min_hole_clearance":0.25,"min_hole_to_hole":0.25,
      "min_microvia_diameter":0.2,"min_microvia_drill":0.1,
      "min_resolved_spokes":2,"min_silk_clearance":0.0,
      "min_text_height":0.8,"min_text_thickness":0.08,
      "min_through_hole_diameter":0.3,"min_track_width":0.1,
      "min_via_annular_width":0.1,"min_via_diameter":0.5,
      "solder_mask_to_copper_clearance":0.0,"use_height_for_length_calcs":True
    },
    "track_widths": [], "via_dimensions": [], "zones_allow_external_fillets":False
  },
  "ipc2581":{"bom_rev":"","dist":"","distpn":"","internal_id":"","mfg":"","mpn":"","sch_revision":""},
  "layer_pairs":[],"layer_presets":[],"viewports":[]
}
j["net_settings"] = {
  "classes":[{
    "bus_width":12,"clearance":0.1,"diff_pair_gap":0.25,"diff_pair_via_gap":0.25,
    "diff_pair_width":0.2,"line_style":0,"microvia_diameter":0.3,"microvia_drill":0.1,
    "name":"Default","pcb_color":"rgba(0, 0, 0, 0.000)","priority":2147483647,
    "schematic_color":"rgba(0, 0, 0, 0.000)","track_width":0.2,"tuning_profile":"",
    "via_diameter":0.6,"via_drill":0.3,"wire_width":6
  }],
  "meta":{"version":5},"net_colors":None,"netclass_assignments":None,"netclass_patterns":[]
}
j.setdefault("pcbnew", {"last_paths":{"idf":"","netlist":"","plot":"","specctra_dsn":"","step":"","vrml":""},"page_layout_descr_file":""})
p.write_text(json.dumps(j, indent=2)+"\n", encoding="utf-8")
print("P21_RULES_INJECTED hole_clearance=0.25 track=0.10 via=0.50/0.30")
