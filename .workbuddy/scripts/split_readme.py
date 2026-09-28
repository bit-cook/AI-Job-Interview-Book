# -*- coding: utf-8 -*-
"""把 6501 行的巨型 README.md 按模块拆分到 docs/ 下，零内容丢失。
用法： python split_readme.py
"""
import os
import re

ROOT = r"E:\study_book\AIGC-Interview-Book"
# 注意：源必须是拆分前的原始 README 备份，而不是被重写后的 README.md
SRC = os.path.join(ROOT, ".workbuddy", "backup", "README_original_20260928.md")

BASE = "https://github.com/km1994/AIGC-Interview-Book/tree/main"


def demote(text, keep_first=True):
    """标题降一级（fence 感知，避免破坏代码块里的 # 注释）。首个标题保持原级。"""
    out, in_fence, seen = [], False, False
    for ln in text.split("\n"):
        if ln.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append(ln)
            continue
        if not in_fence and ln.startswith("#"):
            if keep_first and not seen:
                seen = True
                out.append(ln)
                continue
            out.append("#" + ln)
        else:
            out.append(ln)
    return "\n".join(out)


def fix_links(text):
    """内部模块链接改为相对路径；bare 链接指向主页。"""
    text = text.replace(BASE + "/rag/", "../rag/")
    text = text.replace(BASE + "/agent/", "../agent/")
    text = text.replace(BASE + "/ql/", "../ql/")
    text = text.replace(BASE + "/Harness/", "../Harness/")
    text = text.replace("(" + BASE + ")", "(../README.md)")
    text = text.replace("(" + BASE + ")", "(../README.md)")
    # 原文中的历史遗留问题：仓库根相对路径需要上一级；以及 hhttps 拼写错误
    text = re.sub(r"(!?\[[^\]]*\]\()(?:\./)?img/", r"\1../img/", text)
    text = text.replace("hhttps://", "https://")
    return text


# (输出文件, 起始行, 结束行, 标题, 说明)
SECTIONS = [
    ("docs/rag_160.md", 7, 187, "大模型 RAG 面试高频 160 题",
     "**逐题详解（已开源）**：[基础篇 15 题](../rag/s1_foundation.md) ｜ [分块策略 15 题](../rag/s2_chunking.md) ｜ [Embedding 10 题](../rag/s3_embedding.md)"),
    ("docs/agent_100.md", 188, 406, "大模型 Agent 面试高频 100 题",
     "**逐题详解（已开源）**：[基础篇（1-24 题）](../agent/s1.md)"),
    ("docs/rl_post_training.md", 407, 1148, "大模型强化学习后训练（RL Post-Training）120 题",
     "**逐题详解（已开源）**：[基础概念](../ql/s1_base/s1_base.md) ｜ [PPO 深度解析](../ql/s2_PPO/s2.md) ｜ [DPO 深度解析](../ql/s3_DPO/readme.md)"),
    ("docs/hermes_agent.md", 1149, 2211, "Hermes Agent 面试高频 100 题",
     "**逐题详解（已开源）**：[Harness Engineering 基础](../Harness/s1_harness_base/readme.md) ｜ [自进化核心机制](../Harness/s2_harness_core/readme.md)"),
    ("docs/loop_engineering.md", 2212, 2779, "Loop Engineering 面试高频 100 题",
     "每题附「考察点 + 得分项 + 作答要点」，可直接当模拟面试脚本用。"),
    ("docs/graphrag.md", 2780, 3403, "知识图谱 GraphRAG 面试高频 100 题",
     "每题附「考察点 + 得分项 + 作答要点」，覆盖图谱构建、索引、检索与工程落地。"),
    ("docs/cv_object_detection.md", 3404, 4027, "目标检测与机器视觉 面试高频 100 题",
     "每题附「考察点 + 得分项 + 作答要点」，从传统方法到 DETR 系演进。"),
    ("docs/classic_question_bank.md", 4028, 6501, "经典专题题库（30+ 专题 · 数百考点）",
     "覆盖大模型基础/架构、微调、分布式训练、推理加速、KV Cache、MoE、多模态等经典方向。"),
]

# 经典专题：中文序号 -> 答案所在目录
NUM = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十",
       "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
       "二十一", "二十二", "二十三", "二十四", "二十五", "二十六", "二十七", "二十八", "二十九", "三十",
       "三十一", "三十二", "三十三", "三十四", "三十五", "三十六", "三十七"]

ANS_DIR = {
    "一": "1_LLMs_base_trick/readme.md",
    "二": "2_LLMs_upgrade_trick/readme.md",
    "三": "3_LLMs_finetuning_trick/readme.md",
    "四": "4_langchain_trick/readme.md",
    "五": "5_LLMs_RAG/readme.md",
    "六": "6_peft_trick/readme.md",
    "七": "7_LLMs_inference_trick/readme.md",
    "八": "8_LLMs_pretrain/",
    "九": "9_LLMs_eval_trick/readme.md",
    "十": "10_LLMs_reinforcement_trick/readme.md",
    "十一": "11_LLMs_datasets_trick/readme.md",
    "十二": "12_LLMs_VRAM_trick/readme.md",
    "十三": "13_LLMs_distributed_training_trick/readme.md",
    "十四": "14_LLMs_agent_trick/readme.md",
    "十五": "15_position_encoding/readme.md",
    "十六": "16_LLMs_tokenizer/readme.md",
    "十七": "17_LLMs_optimize_trick/",
    "十八": "18_LLMs_hallucination/readme.md",
    "十九": "19_LLMs_model_compare/readme.md",
    "二十": "20_COT_trick/readme.md",
    "二十一": "21_LLMs_data_breach/readme.md",
    "二十二": "22_LLMs_MOE/readme.md",
    "二十三": "23_LLM_distillation/readme.md",
    "二十四": "24_LLMs_configure_trick/readme.md",
    "二十五": "25_LLMs_token/readme.md",
    "二十六": "26_Multimodal/readme.md",
    "二十七": "27_NLP_trick/readme.md",
    "二十八": "28_other_trick/readme.md",
    "二十九": "29_KV_Cache/",
    "三十": "30_characterLLM/readme.md",
    "三十一": "31_chat_o1/readme.md",
    "三十二": "32_deepseek/interview100.md",
    "三十三": "33_推理大模型/readme.md",
    "三十四": "kimi_1_5/readme.md",
    "三十五": "34_mcp/readme.md",
    "三十六": "36_ContextEngineering/readme.md",
    "三十七": "../README.md",
}


def fix_classic_answers(body):
    """把经典专题里指向仓库根目录的『点击查看答案』按章节改到真实专题目录。"""
    chunks = re.split(r"(?m)^(?=## )", body)
    out = []
    for ch in chunks:
        head = ch.split("\n", 1)[0]
        m = re.search(r"([一二三四五六七八九十]+)、", head)
        target = None
        if m and m.group(1) in ANS_DIR and m.group(1) in NUM:
            target = ANS_DIR[m.group(1)]
        if target:
            ch = ch.replace("[点击查看答案](" + BASE + ")", "[点击查看答案](../%s)" % target)
        out.append(ch)
    return "".join(out)


def reorder_classic(body):
    """经典专题在原 README 中顺序错乱，按中文序号重排，并生成概览清单。"""
    chunks = re.split(r"(?m)^(?=## )", body)
    pre = [c for c in chunks if not c.startswith("## ")]
    secs = [c for c in chunks if c.startswith("## ")]

    def key(ch):
        m = re.search(r"([一二三四五六七八九十]+)、", ch.split("\n", 1)[0])
        if m and m.group(1) in NUM:
            return NUM.index(m.group(1))
        return 999

    secs.sort(key=key)

    def clean_name(ch):
        h = ch.split("\n", 1)[0][3:].strip()
        h = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", h)  # 去掉链接
        h = h.replace(":fire:", "").replace("🔥", "").strip()
        return h

    toc = ["## 本页专题一览（共 %d 个）\n" % len(secs), ""]
    for i, ch in enumerate(secs, 1):
        toc.append("%d. %s" % (i, clean_name(ch)))
    toc.append("")
    toc.append("---")
    toc.append("")

    return "".join(pre) + "\n".join(toc) + "\n".join(secs)


def main():
    with open(SRC, encoding="utf-8") as f:
        lines = f.read().split("\n")
    total = len(lines)
    print("原 README 行数:", total)

    covered = set()
    for out_rel, start, end, title, note in SECTIONS:
        body = "\n".join(lines[start - 1:end])
        covered.update(range(start, end + 1))
        if out_rel.endswith("classic_question_bank.md"):
            body = fix_classic_answers(body)
            body = reorder_classic(body)
        body = fix_links(body)
        # 保留原文标题层级（文件顶层由上面的 H1 承担），避免层级跳级
        header = (
            "# %s\n\n"
            "> 本页属于开源项目《[大模型面试宝典](../README.md)》，返回 [项目主页](../README.md) 查看全部模块导航。\n\n"
            "%s\n\n---\n\n" % (title, note)
        )
        out_path = os.path.join(ROOT, out_rel.replace("/", os.sep))
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(header + body.lstrip("\n") + "\n")
        print("  写出 %-34s 源行 %5d-%-5d -> %d 行" % (out_rel, start, end, header.count("\n") + body.count("\n") + 2))

    # 校验覆盖
    gaps = [i for i in range(1, total + 1) if i not in covered]
    print("未被覆盖的行号（应为空或仅空行）:", gaps[:20], "..." if len(gaps) > 20 else "")


if __name__ == "__main__":
    main()
