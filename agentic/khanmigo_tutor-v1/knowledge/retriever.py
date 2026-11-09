from typing import Any

from knowledge.loader import KnowledgeLoader


class KnowledgeRetriever:
    """
    Retrieves relevant educational knowledge from the
    local knowledge base.
    """

    def __init__(
        self,
        loader: KnowledgeLoader | None = None,
    ) -> None:

        self.loader = (
            loader
            if loader is not None
            else KnowledgeLoader()
        )

        self.knowledge = self.loader.load_all()

    def retrieve(
        self,
        query: str,
        subject: str | None = None,
        topic: str | None = None,
        limit: int = 3,
    ) -> list[dict[str, Any]]:

        if not isinstance(query, str):
            return []

        query = query.strip().lower()

        if not query:
            return []

        query_terms = set(
            query.split()
        )

        scored_results: list[
            tuple[int, dict[str, Any]]
        ] = []

        for item in self.knowledge:

            score = self._calculate_score(
                item=item,
                query=query,
                query_terms=query_terms,
                subject=subject,
                topic=topic,
            )

            if score > 0:
                scored_results.append(
                    (
                        score,
                        item,
                    )
                )

        scored_results.sort(
            key=lambda result: result[0],
            reverse=True,
        )

        return [
            item
            for _, item in scored_results[:limit]
        ]

    def _calculate_score(
        self,
        item: dict[str, Any],
        query: str,
        query_terms: set[str],
        subject: str | None,
        topic: str | None,
    ) -> int:

        score = 0

        concept = str(
            item.get(
                "concept",
                "",
            )
        ).lower()

        definition = str(
            item.get(
                "definition",
                "",
            )
        ).lower()

        explanation = str(
            item.get(
                "explanation",
                "",
            )
        ).lower()

        keywords = [
            str(keyword).lower()
            for keyword in item.get(
                "keywords",
                [],
            )
        ]

        item_subject = str(
            item.get(
                "subject",
                "",
            )
        ).lower()

        item_topic = str(
            item.get(
                "topic",
                "",
            )
        ).lower()

        if subject:
            if item_subject == subject.lower():
                score += 2

        if topic:
            if item_topic == topic.lower():
                score += 2

        if query in concept:
            score += 5

        if query in definition:
            score += 3

        if query in explanation:
            score += 3

        for keyword in keywords:

            if keyword in query:
                score += 5

            keyword_terms = set(
                keyword.split()
            )

            score += len(
                query_terms.intersection(
                    keyword_terms
                )
            ) * 2

        concept_terms = set(
            concept.split()
        )

        score += len(
            query_terms.intersection(
                concept_terms
            )
        ) * 3

        return score
    