import unittest

from planner import generate_company_plan


class PlannerTests(unittest.TestCase):
    def test_plan_contains_five_years(self):
        plan = generate_company_plan(industry="fintech", country="United States")
        self.assertEqual(len(plan["yearly_plan"]), 5)
        self.assertGreater(plan["yearly_plan"][-1]["headcount"], plan["yearly_plan"][0]["headcount"])

    def test_employee_reasons_are_present(self):
        plan = generate_company_plan(industry="manufacturing", country="Germany")
        first_year_employees = plan["yearly_plan"][0]["employees"]
        self.assertTrue(first_year_employees)
        self.assertTrue(all(employee["salary_reason"] for employee in first_year_employees))

    def test_unknown_inputs_fall_back_to_defaults(self):
        plan = generate_company_plan(industry="space mining", country="Moon Base")
        self.assertEqual(plan["matched_profiles"]["industry_name"], "B2B SaaS")
        self.assertEqual(plan["matched_profiles"]["country_name"], "Global Benchmark")


if __name__ == "__main__":
    unittest.main()
