# Security Policy

## Reporting Security Issues

If you discover any security vulnerabilities or issues in the mutapath library, please report them immediately to our security team by sending an email to mat@fax.fyi. We kindly request that you do not publicly disclose any potential security issues until they have been assessed and resolved by our team.

## Supported Versions

Currently, we are actively supporting the following version of mutapath with security updates:

| Version | Supported          |
| ------- | ------------------ |
| ^ 0.17  | :white_check_mark: |
| < 0.17  | :x:                |

For the most secure experience, we highly recommend using the latest supported version of mutapath.

## Dependency Auditing and Updates

To maintain the security of our project, we employ two tools for dependency management:

1. **Packj**: Packj.dev is used to audit our Python packages and detect malicious, vulnerable, abandoned, typo-squatting, and other "risky" packages. This helps us ensure that the dependencies we use are safe and reliable.

2. **Renovate Bot**: We use Renovate Bot to automatically keep our dependencies up-to-date with the latest versions, including security patches. This minimizes the risk of using outdated dependencies with known vulnerabilities.

3. **Fossa**: We use Fossa for license compliance checking and security screening of the mutapath library. Fossa helps us identify potential license conflicts and security vulnerabilities in our dependencies, enabling us to maintain a high level of code quality and security.

## Responsible Disclosure

As mentioned earlier, we take security very seriously and appreciate the efforts of security researchers and contributors in responsibly disclosing potential vulnerabilities. Once we receive a report of a security issue, we will follow the following steps:

1. We will review the report and assess the impact and severity of the issue.
2. We will work on developing and testing a fix for the issue.
3. A security advisory will be prepared, including details about the vulnerability and the fix.
4. The fix will be released in the latest supported version and, if necessary, backported to older supported versions.
5. The security advisory will be made public to the community after the fix has been released, to encourage users to update their installations.

We strive to handle security issues promptly and transparently while ensuring the safety of our users.

Thank you for your support and cooperation in making the mutapath library secure and reliable for all users.
