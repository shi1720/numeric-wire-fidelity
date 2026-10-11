# Literature and overlap assessment

## Claim boundary

The general numeric-interoperability problem is old, and lossless parsing and strict number checks already exist. The artifact's defensible contribution is a schema-conditioned empirical audit, measurement of the schema as well as the argument transport surface, and an actual local MCP wrong-record reproduction. It is not established as a groundbreaking new algorithm or patentable invention. No search can prove absence of all prior work.

## Closest sources examined

1. Möller et al., **Cross-Language Differential Testing of JSON Parsers**, ASIA CCS 2024, DOI [10.1145/3634737.3657003](https://doi.org/10.1145/3634737.3657003). Establishes parser semantic discrepancies and cross-language testing. Rules out a first-discovery claim for numeric transport confusion. Primary paper: https://www.mlsec.org/docs/2024b-asiaccs.pdf
2. Bray, **I-JSON**, RFC 7493 (2015), https://www.rfc-editor.org/rfc/rfc7493 . Explicitly warns about large integers and recommends strings for exact interchange. Rules out invention of the string remedy.
3. Bray, **JSON Data Interchange Format**, RFC 8259 (2017), https://www.rfc-editor.org/rfc/rfc8259 . Allows implementation limits. The audit is not a claim that permitted precision limits violate the standard.
4. Rundgren et al., **JSON Canonicalization Scheme**, RFC 8785 (2020), https://www.rfc-editor.org/rfc/rfc8785 . Shows why serialization domain and numeric conventions matter to canonicalization.
5. Geng et al., **JSONSchemaBench** (2025), https://arxiv.org/abs/2501.10868 . The corpus and existing efficiency/coverage/quality evaluation are attributed to this work; we add a transport-boundary audit rather than claim a new original corpus.
6. Dong et al., **XGrammar**, MLSys 2025, https://proceedings.mlsys.org/paper_files/paper/2025/file/5c20ca4b0b20b0bd2f1d839dc605e70f-Paper-Conference.pdf . Structured generation efficiency is separate from the tested infrastructure boundary. This artifact does not run or compare XGrammar.
7. Lu et al., **Learning to Generate Structured Output with Schema Reinforcement Learning**, ACL 2025, https://aclanthology.org/2025.acl-long.243/ . Model-level schema adherence is separate from transport fidelity. Bibliography metadata was fetched from ACL Anthology.
8. Attouche et al., **Witness Generation for JSON Schema**, PVLDB 15(13), 4002–4014 (2022), DOI 10.14778/3565838.3565852. Primary: https://www.vldb.org/pvldb/vol15/p4002-sartiani.pdf . Complete witness generation is substantially stronger than our local projections, whose reachability limitations are explicit.
9. Habib et al., **Finding Data Compatibility Bugs with JSON Subschema Checking**, ISSTA 2021, DOI 10.1145/3460319.3464796. Schema inclusion/compatibility predates this audit. Source metadata and abstract were inspected; this is not a complete implementation comparison.
10. Berman, **Introducing Bowtie** (2023), https://json-schema.org/blog/posts/bowtie-intro . Validator differentials are established. We do not claim a new meta-validator.
11. Rabinovich and Anaby-Tavor, **On the Robustness of Agentic Function Calling** (2025), https://arxiv.org/abs/2504.00914 . Broader agent robustness evaluation is relevant; our experiment isolates infrastructure after emission.
12. de Jong, **lossless-json**, https://github.com/josdejong/lossless-json , version 4.3.1. Both lossless transport and existing strict numeric safety checks are actual tested baselines. This is a strong existing remedy, not a straw baseline.
13. MCP specification, tools revision 2025-06-18, https://modelcontextprotocol.io/specification/2025-06-18/server/tools . Explains schema and tool-call interfaces. The tested implementation is separately pinned at SDK 1.32.1.

Queries covered LLM tool calling with numeric precision, numeric structured-output fidelity, JSON Schema differential testing, schema witness generation, and MCP numeric transport. Broad search produced substantial prior art. It did not establish an absolute novelty claim for the combined audit.

## Earlier author manuscripts

The local research-folder PDFs were extracted to text and their topics and abstracts reviewed. They cover tool-cache coupling, retry reliability, delegation observability, personal memory, prefix caching, financial exposure routing, delegated deposits, compensation/UndoScope, adaptive contracts, collective capabilities, noisy bandits, private participation, capability visibility, shared-label evaluation, replay, quotas, control, rank fusion, healthcare, batch testing, and tool-coordinate conventions.

This audit uses a different concrete object: numeric schema and argument bytes crossing an MCP parser and serializer. It reuses no earlier manuscript results, figures, code, or experimental data. Conceptual adjacency to UndoScope's general tool-system reliability motivation remains, but numeric transport fidelity is not its compensation mechanism. This local topic review is not a verification of the publication or simultaneous-submission status of every earlier manuscript.

## What would strengthen the contribution

- Full-schema reachable witnesses with a complete witness generator, rather than local projections.
- Cross-SDK and multi-hop interoperability experiments with actual application constraints.
- Raw pre-parse model emissions or privacy-cleared operational traces to estimate practical exposure.
- A genuinely deployed integration and maintenance experience for the Industry Track.
- Substantive human author analysis, verification, and revision, plus venue-required disclosure.

These are missing evidence, not completed work or claims in the manuscript.
