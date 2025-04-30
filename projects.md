---
layout: page
title: Projects
---

## LiSA: LIbrary for Static Analysis

_People involved: Luca Negrini, Vincenzo Arceri, Agostino Cortesi, Pietro Ferrara_

LiSA (Library for Static Analysis) aims to ease the creation and implementation of static analyzers based on the Abstract Interpretation theory. LiSA provides an analysis engine that works on a generic and extensible control flow graph representation of the program to analyze. Abstract interpreters in LiSA are built for analyzing such representation, providing a unique analysis infrastructure for all the analyzers that will rely on it.

Building an analyzer upon LiSA boils down to writing a parser for the language that one aims to analyze, translating the source code or the compiled code towards the control flow graph representation of LiSA. Then, simple checks iterating over the results provided by the semantic analyses of LiSA can be easily defined to translate semantic information into warnings that can be of value for the final user.

## Security and reliability analysis of Smart Contracts

_People involved: Luca Olivieri, Vincenzo Arceri, Luca Negrini, Fabio Tagliaferro, Imran Alam, Badaruddin Chachar, Fausto Spoto (University of Verona, Italy), Agostino Cortesi, Pietro Ferrara_

Blockchain and Smart Contracts are growing more and more in popularity thanks to the hype built around these technologies and the wide range of their applications, such as cryptocurrencies, digital securities and identity management.
The possibility of implementing Smart Contract infrastructures using general-purpose programming languages has become widespread, such as in Cosmos or Hyperledger, where, for example, Go language can be involved to build blockchain applications within these frameworks.
Nevertheless, the design of such languages did not have blockchain development as a goal: their use in such context intrinsically inherits the well known general-purpose programming languages problems. Besides, new blockchain-related vulnerabilities arise in such a context: representatives are transaction ordering and timestamp manipulation.
The objective of this project is to identify and implement advanced and sophisticated program analysis approaches to enhance the quality of applications, remaining in the context of general-purpose programming languages.

- L. Olivieri, L. Negrini, V. Arceri, P. Ferrara, A. Cortesi, F. Spoto: “Static Detection of Untrusted Cross-Contract Invocations in Go Smart Contracts”, in Proceedings of the 40th ACM/SIGAPP Symposium on Applied Computing (SAC), 2025.
- L. Olivieri, L. Negrini, V. Arceri, P. Ferrara, A. Cortesi: “Detection of Read-Write Issues in Hyperledger Fabric Smart Contracts”, in Proceedings of the 40th ACM/SIGAPP Symposium on Applied Computing (SAC), 2025.
- L. Olivieri, V. Arceri, B. Chachar, L. Negrini, F. Tagliaferro, F. Spoto, P. Ferrara, A. Cortesi: “General-Purpose Languages for Blockchain Smart Contracts Development: A Comprehensive Study”, in IEEE Access, vol. 12, pp. 166855-166869, 2024.
- L. Olivieri, L. Negrini, V. Arceri, B. Chachar, P. Ferrara, A. Cortesi: “Detection of Phantom Reads in Hyperledger Fabric," in IEEE Access, vol. 12, pp. 80687-80697, 2024.
- L. Olivieri, F. Spoto: “Software verification challenges in the blockchain ecosystem”, in International Journal on Software Tools for Technology Transfer, vol. 26, 431–444, 2024.
- L. Olivieri, L. Negrini, V. Arceri, F. Tagliaferro, P. Ferrara, A. Cortesi, F. Spoto: “Information flow analysis for detecting non-determinism in blockchain”, in Proceedings of the 37th European Conference on Object-Oriented Programming (ECOOP), 2023.
- L. Olivieri, F. Tagliaferro, V. Arceri, M. Ruaro, L. Negrini, A. Cortesi, P. Ferrara, F. Spoto, E. Talin: “Ensuring determinism in blockchain software with GoLiSA: an industrial experience report”, in Proceedings of the 11th ACM SIGPLAN International Workshop on the State Of the Art in Program Analysis (SOAP), 2022.


# Blockchain Interoperability and Security

_People involved: Aradhita Mukherjee, Luca Olivieri, Agostino Cortesi, Nabendu Chaki (University of Calcutta, India)

As blockchain networks continue to evolve independently, the lack of standardized communication protocols poses significant challenges to scalability and widespread adoption, highlighting the critical need for effective interoperability solutions. This project aims to investigate blockchain interoperability and cross-chain mechanisms, aiming to identify, evaluate, and implement solutions to enable secure and seamless interactions between heterogeneous blockchain networks.

- - L. Olivieri, A. Mukherjee, N. Chaki, A. Cortesi: “Cross-chain Smart Contracts and dApps Verification by Static Analysis: Limits and Challenges”, in Proceedings of the Joint Italian National Conference on Cybersecurity (ITASEC \& SERICS), 2025.
- L. Olivieri, A. Mukherjee, N. Chaki, A. Cortesi: “Blockchain Interoperability through Bridges: A Token Transfer Perspective”, in Proceedings of the 6th International Conference on Blockchain Computing and Applications (BCCA), 2024.

## Static Security Analysis of IoT Systems

_People involved: Agostino Cortesi, Pietro Ferrara, Fausto Spoto (University of Verona, Italy), Amit Mandal (SRM University, Amaravati, India)_

IoT systems usually comprise several software layers: the embedded software running on the physical device (aka thing), some edge application that locally manages a physical system composed by several things and is connected to Internet, some cloud applications providing access to, and storing and visualizing data of the IoT system, and some mobile applications that allows a user to manage the system remotely. Since the overall system interacts with the physical world through sensors and actuators, it is essential to consider the overall system when looking for security vulnerabilities and leakages of sensitive information.

In such context, existing static analysis techniques (and in particular taint analysis) focus on single applications. The goal of this project is to extend such techniques in order to perform inter-program analyses that can detect vulnerabilities due to the interaction between different software layers.

- A. Mandal, P. Ferrara, Y. Khlyebnikov, A. Cortesi, F. Spoto: “Cross-Program Taint Analysis for IoT Systems”, in Proceedings of ACM SAC 2020
- P. Ferrara, A. Mandal, A. Cortesi, F. Spoto: “Cross-Programming Language Taint Analysis for the IoT Ecosystem”, in Electronic Communications of the EASST, vol. 77, 2019 [link]
- A. Mandal, A. Cortesi, A. Sarkar, N. Chaki: “Things as a Service: Service model for IoT”, in Proceedings of INDIN 2019

## String Analysis

_People involved: Martina Olliaro, Vincenzo Arceri, Luca Negrini, Agostino Cortesi, Pietro Ferrara_

Strings are a key ingredient of programming languages. Their usage ranges from composing user messages to performing inter-system communications, every program builds, manipulates, stores and sends strings during its execution.

Both content and structure of strings should be taken into account when investigating the security of programs: a string could be used to open a connection to another host, to execute a query on a database, or to send commands to the operating system. All of these operations should be executed on safe and well-formed strings to avoid both crashes and security breaches. Hence, being able to correctly track string values should be a must for every static analyser which aim to prove the correctness of a program.

Despite the importance of strings, few static analyses are able to approximate the structure and/or the content of strings and even less techniques can capture the relations between them. We aim at designing and implementing new techniques for soundly tracking string values and their relations during a program analysis.

**Keywords:** Program Analysis, Static Analysis, String Analysis, Abstract Interpretation

- V. Arceri, M. Olliaro, A. Cortesi, I. Mastroeni: “Completeness of Abstract Domains for String Analysis of JavaScript Programs”, in Proceedings of ICTAC 2019.
- A. Cortesi, H. Lauko, M. Olliaro, P. Rockai: “String Abstraction for Model Checking of C Programs”, in Proceedings of SPIN 2019.

## Relational Database Watermarking

_People involved: Maikel Lázaro Pérez Gort (Universidad Iberoamericana Puebla, Mexico), Martina Olliaro, Agostino Cortesi, Claudia Feregrino Uribe (National Institute of Astrophysics, Optics and Electronics, Puebla, Mexico)_

Internet causes data to be highly exposed and illicitly used. Relational database watermarking has been proposed as a new field of security, to protect data property value without restricting database portability.

Inserting a watermark into a database provokes acceptable changes that may negatively affect query answers. Indeed, a table resulting from a query executed on a watermarked database may be semantically inconsistent with respect to the one obtained running the same query to the original database or it may not contain the watermark embedded into the database. We aim at designing and implementing new watermarking techniques for preserving both semantics and watermark of tables resulting from queried databases.

**Keywords:** Digital Watermarking, Relational Databases, Semantics Preservation, Query Analysis

- M. L. P. Gort, M. Olliaro, A. Cortesi, C. F. Uribe: “Semantic-driven Watermarking of Relational Textual Databases”, in Expert Systems with Applications,2020
- M. L. P. Gort, C. F. Uribe, A. Cortesi and F. Fernández-Peña: “A Double Fragmentation Approach for Improving Virtual Primary Key-Based Watermark Synchronization”, in IEEE Access, 2020
- M. L. P. Gort, M. Olliaro, A. Cortesi, C. F. Uribe: “Preventing Additive Attacks to Relational Database Watermarking” in Proceedings of CONFENIS 2019
- M. L. P. Gort, C. F. Uribe, A. Cortesi, F. Fernández-Peña: “HQR-Scheme: A High Quality and resilient virtual primary key generation approach for watermarking relational data”, Expert Syst. Appl. 138, 2019

## Security for Robotic Networks

_People involved: Gianluca Caiazza, Ruffin White (Contextual Robotics Institute, UCSD, USA), Agostino Cortesi, and Henrik I. Christensen’ (Contextual Robotics Institute, UCSD, USA)_

In recent years, we observed a growth of cybersecurity threats, especially due to the ubiquitous of connected and autonomous devices commonly defined as Internet of Things (IoT) and Industrial IoT (IIoT).
Considering the sensitive nature of this information there’s a widespread suspicion concerning the way in which these information flows into the infrastructures. Additionally, with the increase of smart cities and connected environments, this critically is going to enlarge.

To address those problems we can distinguish between two lines of research that we explore in parallel, either studying the security and hardening solutions for the devices or focusing on the communication infrastructures.

In this project, we focus on the data-centric analysis of the infrastructure. Its easy to understand the importance of supporting the key property of computer security: Confidentiality, Integrity, Authenticity, Non-reputation, Availability. However, since we are working with IoT devices the way in which these properties are enforced is not trivial. In fact, we need to consider the intrinsic limitations of the devices, either from the power consumption point of view and the actual computational power available. Additionally, since we want to design solutions that could be applied to a wider scope of devices and developers we need to provide mechanisms with a good tradeoff between security and usability.

**Keywords:** Cryptobotics, Security, Network, Static Analysis, Formal Verification

- R. White, G. Caiazza, H. Christensen, A. Cortesi: “SROS1: Using and Developing Secure ROS1 Systems”, Robot Operating System (ROS) (Volume 3), Springer, 2019
- R. White, G. Caiazza, C. Jiang, X. Ou, Z. Yang, A. Cortesi, H. Christensen: “Network Reconnaissance and Vulnerability Excavation of Secure DDS Systems”, EuroS&PW 2019 (SSIoT), IEEE Computer Society Conference Publishing Services
- R. White, G. Caiazza, A. Cortesi, H. Christensen: “Procedurally Provisioned Access Control for Robotic Systems”, IEEE/RSJ International Conference on Intelligent Robots and Systems 2018 

## VIR2EM

_People involved: Gianluca Caiazza, Agostino Cortesi, Alvise Spanò, Pietro Ferrara_

The VIR2EM project (VIrtualization and Remotization for Resilient and Efficient Manufacturing) proposes to use virtualization technologies for processes, systems, and resources to foster remote operations. Funded by Regione Veneto as part of the Reti Innovative Regionali (RIR) initiative, it foresees a strong collaboration between companies and the world of research with the University of Padua, Verona, and the University of Venice Ca’ Foscari.

The corporate partnership also provides a Public Research Body (t2i) with extensive experience in technology transfer activities towards the business market and the presence of a large number of knowledge-intensive service providers (KIBS): beanTech, Qascom, Statwolf Data Science, Uquido, Xteam; in addition to companies leaders in their production sector and comprehensive national and international visibility (Electrolux, Galdi, Sipa, Sperotto Rimar, Zamperla).

The strong integration between academic partners, service providers, and end-users favors transferring and sharing knowledge. The project’s general goals include: maximize the efficiency of production systems under normal operating conditions, maintain and ease the restart of operations downstream in the event of emergencies, guaranteeing flexibility and predictive capacity.

In this scenario, our team focuses on cybersecurity that lives at the computational and applications level, particularly relevant in organizations and productions with remote resources and operations. With the goal of developing tools to analyze the security of remote and virtualized systems and to remedy dormant vulnerabilities via formal static and dynamic analysis.
