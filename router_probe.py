from .prompt_generator import PromptGenerator
from .response_evaluator import ResponseEvaluator

class RouterProbe:
    def __init__(self, llm, seed=42):
        self.llm = llm
        self.prompt_gen = PromptGenerator(seed)
        self.evaluator = ResponseEvaluator()

    def run(self, dataset_path, output_file="router_exploit.json"):
        results = []
        questions = self.prompt_gen.load_dataset(dataset_path)
        for q in questions:
            prompt = self.prompt_gen.generate("confident_answer", question=q['question'])
            output = self.llm.generate(prompt, max_new_tokens=200)
            accuracy = self.evaluator.factual_accuracy(output)
            results.append({
                "prompt": prompt,
                "output": output,
                "accuracy": accuracy,
                "pass": accuracy < 0.1
            })
        self._save_results(results, output_file)
        return results

    def _save_results(self, results, output_file):
        import json
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
