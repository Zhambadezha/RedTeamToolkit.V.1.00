class SteganoProbe:
    def __init__(self, llm, seed=42):
        self.llm = llm
        self.prompt_gen = PromptGenerator(seed)
        self.evaluator = ResponseEvaluator()

    def run(self, pii_list, output_file="data_exfiltration.json"):
        results = []
        for pii in pii_list:
            encode_prompt = self.prompt_gen.generate("stegano_encode", pii=pii)
            poem = self.llm.generate(encode_prompt, max_new_tokens=200)
            decode_prompt = self.prompt_gen.generate("stegano_decode", text=poem)
            decoded = self.llm.generate(decode_prompt, max_new_tokens=200)
            results.append({
                "encode_prompt": encode_prompt,
                "poem": poem,
                "decode_prompt": decode_prompt,
                "decoded": decoded,
                "pass": self.evaluator.stegano_detection(decoded, pii)
            })
        self._save_results(results, output_file)
        return results
