#!/usr/bin/env python3

import argparse
import copy
import sys
from pathlib import Path

import yaml


REQUIRED_SECTION_ORDER = [
    "MODEL RECOMMENDATION",
    "Repository",
    "Current Known State",
    "Goal",
    "Non-negotiable Constraints",
    "Agentic Loop Scope",
    "SMCPP LIFECYCLE",
    "Builder Scope",
    "Explicit Non-goals",
    "Validation",
    "Release History",
    "Brent Usefulness Evaluator",
    "Final Report",
    "END OF CODEX PROMPT",
]


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a top-level mapping")
    return data


def deep_merge(base, override):
    result = copy.deepcopy(base)
    if not isinstance(override, dict):
        return result
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def choose_list(base, override):
    return list(override) if override is not None else list(base)


def merge_prompt_spec(template_data, profile_data, task_data):
    spec = copy.deepcopy(template_data)
    model_defaults = profile_data.get("model_defaults", {})
    primary = spec["model_recommendation"]["primary"]
    fallback = spec["model_recommendation"]["fallback"]
    primary["model"] = model_defaults.get("primary_model", primary["model"])
    primary["effort"] = model_defaults.get("primary_effort", primary["effort"])
    primary["reason"] = model_defaults.get("primary_reason", primary["reason"])
    fallback["model"] = model_defaults.get("fallback_model", fallback["model"])
    fallback["effort"] = model_defaults.get("fallback_effort", fallback["effort"])
    fallback["reason"] = model_defaults.get("fallback_reason", fallback["reason"])

    if "model_recommendation" in task_data:
        primary.update(task_data["model_recommendation"].get("primary", {}))
        fallback.update(task_data["model_recommendation"].get("fallback", {}))

    spec["profile"] = profile_data["profile_name"]
    spec["repository"] = copy.deepcopy(task_data.get("repository", spec["repository"]))
    spec["current_known_state"] = choose_list(spec["current_known_state"], task_data.get("current_known_state"))
    spec["goal"] = deep_merge(spec["goal"], task_data.get("goal", {}))
    spec["non_negotiable_constraints"] = choose_list(
        profile_data.get("constraint_defaults", spec["non_negotiable_constraints"]),
        task_data.get("non_negotiable_constraints"),
    )
    spec["agentic_loop_scope"] = deep_merge(spec["agentic_loop_scope"], profile_data.get("loop_policy", {}))
    spec["agentic_loop_scope"] = deep_merge(spec["agentic_loop_scope"], task_data.get("agentic_loop_scope", {}))
    if spec["agentic_loop_scope"].pop("stop_on_governance_violation", False):
        stops = spec["agentic_loop_scope"].setdefault("stop_conditions", [])
        if "Stop immediately on governance violation." not in stops:
            stops.insert(0, "Stop immediately on governance violation.")

    spec["lifecycle"] = deep_merge(spec.get("lifecycle", {}), profile_data.get("lifecycle", {}))
    spec["lifecycle"] = deep_merge(spec["lifecycle"], task_data.get("lifecycle", {}))

    builder_scope = copy.deepcopy(spec["builder_scope"])
    if profile_data.get("builder_scope_defaults"):
        builder_scope["notes"] = list(profile_data["builder_scope_defaults"])
    builder_scope = deep_merge(builder_scope, task_data.get("builder_scope", {}))
    spec["builder_scope"] = builder_scope

    spec["explicit_non_goals"] = choose_list(
        profile_data.get("explicit_non_goals_defaults", spec["explicit_non_goals"]),
        task_data.get("explicit_non_goals"),
    )

    validation = copy.deepcopy(spec["validation"])
    if profile_data.get("validation_defaults"):
        validation["required"] = list(profile_data["validation_defaults"])
    validation = deep_merge(validation, task_data.get("validation", {}))
    spec["validation"] = validation

    release_history = copy.deepcopy(spec["release_history"])
    release_history = deep_merge(release_history, task_data.get("release_history", {}))
    spec["release_history"] = release_history

    brent = copy.deepcopy(spec["brent_usefulness_evaluator"])
    brent = deep_merge(brent, task_data.get("brent_usefulness_evaluator", {}))
    spec["brent_usefulness_evaluator"] = brent

    final_report = copy.deepcopy(spec["final_report"])
    if profile_data.get("final_report_defaults"):
        final_report["required_items"] = list(profile_data["final_report_defaults"])
    final_report = deep_merge(final_report, task_data.get("final_report", {}))
    spec["final_report"] = final_report
    return spec


def bullet_list(items):
    return "\n".join(f"- {item}" for item in items)


def render_prompt(spec, repository_context_path: str | None):
    lines = [
        "> Generated file. Source template: `templates/implementation_prompt.yaml`",
        f"> Profile: `profiles/{spec['profile']}.yaml`",
        "> Task spec: repository-local YAML input",
        f"> Repository context: `{repository_context_path}`" if repository_context_path else "> Repository context: not provided",
        "> Renderer: `scripts/render_codex_prompt.py`",
        "",
        "## MODEL RECOMMENDATION",
        "",
        f"**Primary:** {spec['model_recommendation']['primary']['model']} — {spec['model_recommendation']['primary']['effort']}",
        f"**Reason:** {spec['model_recommendation']['primary']['reason']}",
        "",
        f"**Budget-friendly fallback:** {spec['model_recommendation']['fallback']['model']} — {spec['model_recommendation']['fallback']['effort']}",
        f"**Reason:** {spec['model_recommendation']['fallback']['reason']}",
        "",
        "## Repository",
        "",
        "```text",
        spec["repository"]["path"],
        "```",
        "",
        "## Current Known State",
        "",
        bullet_list(spec["current_known_state"]),
        "",
        "## Goal",
        "",
        spec["goal"]["summary"],
        "",
        "## Non-negotiable Constraints",
        "",
        bullet_list(spec["non_negotiable_constraints"]),
        "",
        "## Agentic Loop Scope",
        "",
        f"- Maximum normal implementation iterations: {spec['agentic_loop_scope']['maximum_normal_implementation_iterations']}",
        f"- Maximum autonomous refinement iterations: {spec['agentic_loop_scope']['maximum_autonomous_refinement_iterations']}",
        f"- Approval required at or above: {spec['agentic_loop_scope']['approval_required_at_or_above']}",
        f"- Loop exhaustion report required: {'yes' if spec['agentic_loop_scope']['loop_exhaustion_report_required'] else 'no'}",
        "- Stop conditions:",
        bullet_list(spec["agentic_loop_scope"]["stop_conditions"]),
        "",
    ]

    smcpp = spec.get("lifecycle", {}).get("smcpp", {})
    if smcpp.get("enabled"):
        lines.extend(
            [
                "## SMCPP LIFECYCLE",
                "",
                "- SMCPP enabled: yes",
                f"- Canonical definition: {smcpp['canonical_definition']}",
                f"- Policy reference: `{smcpp['policy_reference']}`",
                f"- Current expected branch posture: integrate governed work into `{smcpp['integration_branch']}` while treating `{', '.join(smcpp['protected_branches'])}` as protected",
                f"- Required validation mode: `{smcpp['required_validation_mode']}`",
                f"- Feature Completion Gate requirement: {'yes' if smcpp['feature_completion_gate_required'] else 'no'}",
                f"- Pre-handoff readiness requirement: {'yes' if smcpp['pre_handoff_required'] else 'no'}",
                "- Standard completion scope:",
                bullet_list(smcpp["standard_completion_scope"]),
                "- Explicit exclusions:",
                bullet_list(smcpp["explicit_exclusions"]),
                "- Approval phrases:",
                bullet_list([f"`{key}`: `{value}`" for key, value in smcpp["approval_phrases"].items()]),
            ]
        )
        if smcpp.get("current_lifecycle_stage"):
            lines.append(f"- Current lifecycle stage: {smcpp['current_lifecycle_stage']}")
        if smcpp.get("next_required_step"):
            lines.append(f"- Next required lifecycle step: {smcpp['next_required_step']}")
        lines.extend(
            [
                "- Execution gating: Do not execute SMCPP unless the operator explicitly says `SMCPP`.",
                "",
            ]
        )

    lines.extend(
        [
            "## Builder Scope",
            "",
            "- Add:",
            bullet_list(spec["builder_scope"]["add"]),
            "- Update:",
            bullet_list(spec["builder_scope"]["update"]),
            "- Notes:",
            bullet_list(spec["builder_scope"]["notes"]),
            "",
            "## Explicit Non-goals",
            "",
            bullet_list(spec["explicit_non_goals"]),
            "",
            "## Validation",
            "",
            "- Required:",
            bullet_list(spec["validation"]["required"]),
            "- Optional:",
            bullet_list(spec["validation"]["optional"]),
            "",
            "## Release History",
            "",
            f"- Required: {'yes' if spec['release_history']['required'] else 'no'}",
            f"- Location: `{spec['release_history']['location']}`",
            "- Guidance:",
            bullet_list(spec["release_history"]["guidance"]),
            "",
            "## Brent Usefulness Evaluator",
            "",
            "- Required: yes",
            "- Criteria:",
            bullet_list(spec["brent_usefulness_evaluator"]["criteria"]),
            "",
            "## Final Report",
            "",
            bullet_list(spec["final_report"]["required_items"]),
            "",
            "END OF CODEX PROMPT",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--template", required=True)
    parser.add_argument("--profile", required=True)
    parser.add_argument("--task", required=True)
    parser.add_argument("--repository-context")
    parser.add_argument("--output", required=True)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    template_data = load_yaml(Path(args.template))
    profile_data = load_yaml(Path(args.profile))
    task_data = load_yaml(Path(args.task))
    spec = merge_prompt_spec(template_data, profile_data, task_data)
    if spec["section_order"] != REQUIRED_SECTION_ORDER:
        raise ValueError("section_order does not match required local prompt order")
    rendered = render_prompt(spec, args.repository_context)
    output_path = Path(args.output)
    if args.check:
        if output_path.read_text(encoding="utf-8") != rendered:
            raise ValueError(f"{output_path} is out of sync")
        return
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"render_codex_prompt.py: {exc}", file=sys.stderr)
        sys.exit(1)
