# Luma Foundry — Non-Watermark IP Protection Research Notes

## Verified primary-source findings

WIPO states that copyright protection generally arises automatically when an original work exists, while national registration or deposit systems may provide useful evidence of a claim. WIPO also recommends copyright notices, proof-of-creation records, time stamps, access controls, encryption, and lower-quality public preview versions as possible digital-work safeguards. Copyright protects original expression rather than underlying ideas or methods.[1]

WIPO describes trade-secret protection as dependent on commercially valuable information remaining limited to a defined group and being subject to reasonable confidentiality measures. It lists confidentiality agreements, robust IT security, and controlled document access as common preventive measures; source code can be among the protected confidential information.[2]

WIPO explains that trademark registration may provide exclusive rights to a registered brand sign within the relevant territory and classes, subject to national or regional procedures. Trademark protection is therefore relevant to the `Luma Foundry` name and distinctive brand marks, not to the complete source code of each template.[3]

GitHub supports verified commit and tag signatures using GPG, SSH, or S/MIME. Sigstore provides tools for signing and verifying released software artifacts and records verification metadata in a tamper-resistant transparency log. These mechanisms support release provenance and integrity; they do not themselves grant or prove legal ownership.[4] [5]

SPDX is an open ISO/IEC standard for representing software components, licences, and related supply-chain information in a Software Bill of Materials. It is appropriate for recording third-party dependencies and required notices in each commercial release.[6]

Amazon S3 presigned URLs provide time-limited object access without exposing storage credentials. AWS cautions that a presigned URL is a bearer token and must be protected; it is therefore a delivery-control layer, not a licence or anti-copy guarantee.[7]

## Luma Foundry decision implications

The strongest near-term system is layered: immutable release hashes and signed tags; complete asset and dependency licence registers; buyer-specific licence and delivery manifests; time-limited downloads; restricted pre-release source access; brand/trademark protection; and evidence-led monitoring and takedown procedures. Browser restrictions and code obfuscation should not be represented as meaningful IP protection.

## References

[1]: https://www.wipo.int/en/web/copyright/protection
[2]: https://www.wipo.int/en/web/trade-secrets
[3]: https://www.wipo.int/en/web/trademarks
[4]: https://docs.github.com/en/authentication/managing-commit-signature-verification
[5]: https://www.sigstore.dev/
[6]: https://spdx.dev/
[7]: https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html
