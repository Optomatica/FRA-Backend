import os                                                                                                                                                                                     
import pandas as pd                                                                                                                                                                           
from dotenv import load_dotenv                                                                                                                                                                
from typing import List, Dict                                                                                                                                                                 
from pinecone import Pinecone                                                                                                                                                                 
from openai import OpenAI    
from mistralai.client import MistralClient    
import json
import re                                                                                                                                                
                                                                                                                                                                                              
load_dotenv()                                                                                                                                                                                 
                                                                                                                                                                                              
# Environment variables                                                                                                                                                                       
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")                                                                                                                                                  
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")                                                                                                                                                
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")                                                                                                                                              
INDEX_NAME = "opto-fra"                                                                                                                                                                       
                                                                                                                                                                                              
# Initialize Pinecone                                                                                                                                                                         
pc = Pinecone(api_key=PINECONE_API_KEY)                                                                                                                                                       
index = pc.Index(INDEX_NAME, namespace="opto_fra_1")                                                                                                                                                                  
                                                                                                                                                                                              
# Initialize                                                                                                                                                                           
mistral_client = MistralClient(api_key=MISTRAL_API_KEY)    

# Context to be used when expanding the query
CONTEXT="""

    # Digital Financial Technology Regulations - Legal Framework

    ## Section II: Digital Identity Controls

    ### 1. Core Digital Identity Process
    Digital identity is controlled through three sub-processes:
    - **Identification** (التحديد)
    - **Verification** (التحقق) 
    - **Authentication** (المصادقة)

    ### 2. Digital Identity Creation and Renewal
    - Digital identity creation/renewal requires completing identification, verification, and authentication processes on physical identity
    - Platform access requires completing identification, verification, and authentication processes on digital identity

    ### 3. Multi-Factor Requirements
    Sub-processes must rely on more than one qualitative group of identification, verification, and authentication factors.

    ### 4. Three Qualitative Factor Groups

    #### A. Knowledge Factor Group (مجموعة عامل المعرفة)
    - Username
    - Password
    - Personal question answers

    #### B. Possession Factor Group (مجموعة عامل الحيازة)
    - Identity document
    - Email account
    - Mobile phone number
    - Device number or SIM card number linked to mobile
    - Non-cash payment account
    - Certified electronic signature

    #### C. Presence and Vitality Factor Group (مجموعة عامل الوجود والحيوية)
    - Biometric characteristics:
    - Face recognition
    - Voice recognition
    - Fingerprints
    - Palm geometry
    - Eye/retina scan
    - Vitality reaction
    - Geographic location identifiers
    - Cyber location identifiers
    - Transaction time identifiers

    ### 5. Requirements for Digital Identity Creation/Renewal

    #### Mandatory Requirements:
    - **Four elements minimum** from Possession Factor Group, including:
    - Identity document
    - Email account
    - Mobile phone number
    - Device number
    - **Three elements minimum** from Presence/Vitality Factor Group, including:
    - Face biometric characteristics
    - Vitality reaction
    - Geographic location identifiers
    - Determine cyber location and transaction time
    - Create/update three Knowledge Factor elements:
    - Username
    - Password
    - Personal question answers
    - Electronic linking with systems designated by the Authority under Law No. 5 of 2022

    ### 6. Subsequent Authentication Requirements (Post-Creation)

    #### Mandatory Requirements:
    - **Two elements** from Knowledge Factor Group:
    - Username
    - Password
    - **One element minimum** from Possession Factor Group:
    - Device number, OR
    - Mobile phone number, OR
    - Email account
    - **One element minimum** from Presence/Vitality Factor Group:
    - Biometric characteristics, OR
    - Vitality reaction, OR
    - Geographic location identifiers
    - Determine cyber location and transaction time
    - Review changes through electronic record and take appropriate actions
    - Electronic linking with Authority systems under Law No. 5 of 2022

    ### 7. Three Trust Levels for Digital Identity

    #### A. Basic Trust Level (درجة الثقة الأساسية)
    - **Minimum requirements:**
    - 2 elements from Knowledge Factor Group
    - 3 elements from Presence/Vitality Factor Group
    - 4 elements from Possession Factor Group
    - **Used for:** Low-risk operations

    #### B. General Trust Level (درجة الثقة العامة)
    - **Requirements:** Basic Trust Level factors PLUS
    - Non-cash payment account possession
    - **Used for:** Medium-risk operations

    #### C. High Trust Level (درجة الثقة المرتفعة)
    - **Requirements:** General Trust Level factors PLUS
    - Certified electronic signature possession
    - **Used for:** High-risk operations

    **Note:** Service providers determine operation risk levels according to Authority guidelines.

    ---

    ## Section III: Digital Contract Controls

    ### 1. Service Provider Obligations
    Service providers must verify:
    - Customer identity
    - Customer consent
    - Electronic contract storage

    #### A. Customer Identity Verification
    Apply same digital identity controls required for platform access (Section II requirements)

    #### B. Customer Consent Verification
    Verify customer consent ensuring:
    - Legal capacity and will
    - Offer and acceptance provisions
    - Proof of customer awareness of all contract terms
    - Compliance with digital contract special nature

    #### C. Electronic Contract Storage
    Store contract with all pre-conclusion stages and timings in digital record using appropriate encryption technology approved by the Authority

    ### 2. Risk-Based Contract Requirements

    #### For Low/Medium Risk Transactions:
    - Use appropriate encryption technology
    - Include verified electronic payment account data
    - Contract must include customer consent for account use
    - Complete transactions through Central Bank-approved electronic payment service providers

    #### For High Risk Transactions:
    - Use electronic signature technology with public-private key encryption
    - Signature must be from Authority-licensed electronic signature certification providers
    - Authority determines transaction values not requiring public-private key electronic signature

    ---

    ## Section IV: Digital Record Requirements

    ### 1. Digital Record Structure
    Each digital platform must have a digital record, divisible into sub-records for specific operation types:

    #### A. Digital Identity Operations Record
    - Create, modify, update, renew, cancel digital identity transactions

    #### B. Customer Recognition Operations Record  
    - Create, modify, update, renew, cancel digital customer account transactions

    #### C. Electronic Contracting Operations Record
    - Create, modify, update, renew, cancel digital non-banking financial product account transactions

    #### D. Financial Product Transaction Operations Record
    - Create, modify, update, renew, cancel transactions on digital non-banking financial product accounts

    ### 2. Digital Record Storage and Retrieval Capabilities
    Must store and retrieve:
    - Transaction data and details with event recording
    - Party information, timings, content, results for state changes
    - Related digital documents as input, attachment, or output

    ### 3. Technical Requirements

    #### Security and Integrity:
    - Use Authority-approved encryption technology
    - Ensure confidentiality and integrity of digital record contents
    - Implement mechanisms preventing content modification after storage

    #### Storage Requirements:
    - Provide adequate storage capacity
    - Maintain records for minimum 5 years after digital asset expiry
    - Notify asset owners/beneficiaries before deletion
    - Retain records during legal proceedings until resolution
    - May store in offline environments or dispose with prior Authority approval

    #### Database Management:
    - Use appropriate database and file management systems
    - Ensure maximum reliability levels
    - Implement failure management mechanisms
    - Apply business continuity and disaster recovery mechanisms

    #### Verification and Reporting:
    - Provide verification, search, summary, and reporting capabilities
    - Maintain security and protection requirements
    - Log verification and search operations with timestamps

    ### 4. Format Standards
    - Comply with "System Log" format (RFC 5424) from Internet Engineering Task Force (IETF)
    - Alternative formats permitted with Authority approval

    ### 5. Digital Forensic Capabilities
    Digital record must enable digital forensic analysis through:

    #### Infrastructure Components:
    - Network devices
    - Computer systems
    - Storage media
    - Virtual and container environment management systems
    - Operating systems
    - Database management systems
    - Access control systems

    #### Information System Components:
    - Applications
    - Databases
    - Records accessible to authorized technical personnel (system administrators, forensic investigators, developers)

    ### 6. Cloud Computing Requirements
    For public or private cloud computing models:
    - Obtain Authority approval
    - Ensure complete separation between virtual environments for each client

    ### 7. Chain of Custody Requirements
    Digital record must prove and document sequence of custody using:
    - Encryption technologies or Authority-approved alternatives
    - Maintain:
    - Data privacy
    - Non-modification (no deletion, addition, or alteration)
    - Non-repudiation from platform manager
    - Non-repudiation from platform user

    ### 8. Blockchain and Smart Contracts
    - Electronic recording, electronic signature, and smart contract enforcement through blockchain or distributed ledger technology are permitted
    - Smart contracts are programs tracking contractual states that change based on pre-agreed events
    - May operate through blockchain technology

    ### 9. Implementation Options
    Digital records may be implemented on centralized or distributed technologies according to Appendix 2 requirements

    ### 10. Legal Status
    Referenced data has the validity of official documents in proof from the date of storage in the digital record

    ---

    ## Section IV-A: Distributed Ledger Technology Implementation

    ### 1. Distributed Ledger Permission
    - Digital records may be implemented using "distributed ledger technology" or "blockchain technology"
    - Requires Authority approval
    - Must designate "General Coordinator" for each "distributed ledger"
    - Coordinator responsible for involving authorized technical personnel

    ### 2. Distributed Ledger Technology Requirements
    - Requires peer-to-peer computational and storage network
    - Consensus/agreement algorithms needed
    - Reliable replication of "constraint sets" across distributed network units

    ### 3. Distributed Ledger System Definition
    - Digital database for storing data/information on distributed computational and storage units
    - Each participating unit has equal influence authority
    - Requires unanimous consent from all participating units
    - Automatic updates distributed to all network units upon agreement

    ### 4. Blockchain System Definition
    - Decentralized, replicated digital transaction database
    - Transaction constraints "agreed upon" by peer network members
    - Block structure chronologically sequenced
    - Mathematically secured using codes derived from previous digital transaction information
    - May be public, private, permissioned, or permissionless
    - May be linked to tokenized or non-tokenized encrypted shared assets

    ---

    ## Section V: Financial Technology Usage Areas

    ### 1. Mandatory Financial Technology Areas
    The Authority determines essential areas for financial technology use in non-banking financial activities:

    #### A. Electronic Identification, Verification, and Authentication Operations
    #### B. Electronic Customer Recognition Operations  
    #### C. Electronic Non-Banking Financial Product Contracting Operations
    #### D. Electronic Recording, Storage, and Retrieval from Digital Records Operations

    ### 2. Optional Areas
    The Authority determines additional permissible areas for financial technology use in non-banking financial activities.

    ---

    ## Section VI: Compliance Requirements

    ### 1. Semi-Annual Reporting
    - Prepare semi-annual "Audit Results and Error Rates" report
    - Consider service provider's business nature and volume
    - Submit Authority-approved report from Board of Directors within 4 weeks of period end
    - Apply to all financial technology operations and areas per Appendix 3 format

    ### 2. Continuous Compliance Monitoring
    - Ensure continuous system compatibility with workflow management and execution
    - Comply with financial technology areas approved in Sections III and IV
    - Adhere to "Digital Identity," "Digital Contracts," and "Digital Records" controls
    - Apply to non-banking financial services through digital platforms

    ### 3. Quarterly Disclosure Requirements
    - Disclose material events causing non-compliance and causes
    - Report remediation actions taken
    - Report material system modifications with reasons, especially for weakness remediation
    - Submit Board-approved quarterly report within 15 days of period end

    ---

    ## Legal Framework Context
    These regulations operate under:
    - **Law No. 5 of 2022** regarding regulation and development of financial technology use in non-banking financial activities
    - **Authority oversight** for financial technology implementation
    - **Central Bank coordination** for payment services
    - **Information Technology Industry Development Authority** for electronic signature certification

    ---

    ## Section VII: Registry Registration Conditions

    ### Registration Requirements
    Considering laws and decisions regulating financial technology use in non-banking financial activities, registry registration requires the following conditions:

    #### 1. Corporate Structure Requirements
    - Must be an Egyptian joint-stock company, OR
    - Any other legal form with commitment to convert to joint-stock company within maximum 12 months from registry registration date

    #### 2. Capital Requirements
    - Company capital must not be less than minimum amount determined by the Authority

    #### 3. Experience Requirements
    - Must have appropriate expertise according to the field, as determined by the Authority

    #### 4. Governance Requirements
    - Must have necessary governance rules and applications
    - Ensure robust internal control environment within the company

    #### 5. Technology Requirements
    - Must have necessary technological capabilities to ensure:
    - Customer data security for contracting parties
    - Privacy and confidentiality protection for service-related data
    - Necessary corrective procedures when performance defects appear
    - Event logging for related incidents

    #### 6. Insurance Requirements
    - Commitment to conclude insurance policy against:
    - Technological risks
    - Professional liability

    #### 7. Registration Fees
    - Payment of registration service fee: 25,000 EGP per field

    ---

    ## Section VIII: Registry Registration Application Procedures

    ### Application Submission Requirements
    Registration applications must be submitted using Authority-prepared forms, with minimum attachments demonstrating:

    #### 1. Service Description
    - Nature and specification of the service for which registration is requested

    #### 2. Technical Security Methods
    - Company's technical methods to ensure:
    - Information security
    - Cybersecurity

    #### 3. Regulatory Reports
    - Various regulatory reports provided by outsourcing service provider to contracting party
    - Ensure compliance with Authority rules and regulations
    - Apply Law No. 5 of 2022 regarding regulation and development of financial technology use in non-banking financial activities

    #### 4. Information Systems Governance
    - Information systems governance methods including:
    - Requirements specified in Financial Regulatory Authority decisions

    ### Application Processing Timeline
    - Authority must decide on registration application within **30 days** from submission date with complete supporting documents

    ---

    ## Section IX: Continued Registry Registration Conditions

    ### Ongoing Obligations for Outsourcing Service Providers

    #### 1. Contract Notification Requirements
    - Notify Authority (as determined by Authority) when concluding:
    - Any outsourcing contract, OR
    - Material modifications to existing contracts

    #### 2. Compliance Requirements
    - Achieve contracting party compliance requirements according to Authority regulations
    - Comply with regulations governing outsourced operations

    #### 3. Data Retention Restrictions
    - **Prohibited** from retaining:
    - Contracting party customer data
    - Executed operation data after completion

    #### 4. Information Disclosure Requirements
    - Provide Authority with any information or documents necessary for Authority operations

    #### 5. Regulatory Inspection Notifications
    - Notify contracting party and Authority when any supervisory body requests:
    - Regulatory review and inspection activities
    - Results of such activities

    #### 6. Corrective Action Requirements
    - Implement necessary corrective procedures when performance defects appear
    - Record related events
    - Enable contracting party and Authority to review such events

    ---

    ## Section X: Registration Period and Renewal

    ### Registration Duration
    - Registration period: **One year**, renewable under same conditions

    ### Grace Period
    - Registered entities have **one month grace period** calculated from day following registry registration expiry date
    - From day following grace period expiry without renewal, company is considered **unregistered**

    ### Authority Discretion
    - Authority Board of Directors may extend timeframes mentioned in this paragraph

    ### Renewal Restrictions
    #### Administrative Measures Impact:
    - **Cannot renew registration** for entities subject to administrative measures (except warnings)
    - Must wait **one year** from administrative measure decision date

    #### Previous Removal Impact:
    - **Cannot register** entities previously removed from registry
    - Must wait **two years** from removal date

    ### Exception Authority
    - Authority Board of Directors may make exceptions to above timeframes
    - Based on justifications submitted by outsourcing service provider

    ---

    ## Section XI: Administrative Measures

    ### Authority Powers
    Authority Board of Directors may take following measures when service provider:
    - Loses any registration or continuation conditions, OR
    - Violates any obligations established in laws and decisions regulating financial technology use in non-banking financial activities for outsourcing service providers

    ### Available Administrative Measures

    #### 1. Warning (التنبيه)
    - Direct warning regarding attributed violations
    - Specify time period necessary to remove violation causes

    #### 2. Temporary Suspension (الإيقاف المؤقت)
    - Temporary registry registration suspension
    - Maximum duration: **one year**

    #### 3. Board召集 (دعوة مجلس الإدارة)
    - Summon company Board of Directors or management (as applicable)
    - Review attributed violations
    - Require necessary actions to remove violations

    #### 4. Registry Removal (الشطب)
    - Complete removal from registry

    ---

    ## Key Definitions
    - **Digital Identity**: Electronic representation requiring multi-factor authentication
    - **Digital Contract**: Electronic agreement with verified identity and consent
    - **Digital Record**: Encrypted, immutable transaction and document storage system
    - **Trust Levels**: Risk-based security requirements (Basic/General/High)
    - **Blockchain/DLT**: Distributed ledger technologies for secure record-keeping
    - **Outsourcing Service Provider**: Entity providing financial technology services under outsourcing arrangements
    - **Contracting Party/العاهد**: Entity that contracts outsourcing services
    - **Registry Registration**: Official registration in Authority-maintained registry for financial technology service providers

    ---

    
    ### Lifecycle Processes (LP1-LP5)
    ITG-F ITSM: LP1: set "the startgeic directon"
    ITG-F ITSM: LP2: design "new or changed services"
    ITG-F ITSM: LP3: build "new or changes services"
    ITG-F ITSM: LP4: operate "the services"
    ITG-F ITSM: LP5: improve "the services"

    ### Supporting Processes (SP1-SP12)
    ITG-F ITSM: SP1: set-up & maintain the "Service Management System"
    ITG-F ITSM: SP2: maintain the "Service Portfolio"
    ITG-F ITSM: SP3: manage "Customer Relations"
    ITG-F ITSM: SP4: manage "Configuration Information"
    ITG-F ITSM: SP5: assess & coordinate "changes"
    ITG-F ITSM: SP6: manage "Projects"
    ITG-F ITSM: SP7: ensure "Security"
    ITG-F ITSM: SP8: prepare for "Disaster Events"
    ITG-F ITSM: SP9: ensure "compliance"
    ITG-F ITSM: SP10: manage "Human Resources"
    ITG-F ITSM: SP11: manage "Suppliers"
    ITG-F ITSM: SP12: manage "Service" Financials"

    ---

    ### Life-cycle Risk Processes (LRP1-LRP4)
    TRM-F LRP1: Framing "RISK"
    TRM-F LRP2: Assessing "RISK"
    TRM-F LRP3: Responding to "RISK"
    TRM-F LRP4: Monitoring "RISK"

    ### Security Control Processes (SCP1-SCP7)
    TRM-F SCP1: Prepare "Executive & Opeational Levels"
    TRM-F SCP2: Categorize "Systems"
    TRM-F SCP3: Select "Controls"
    TRM-F SCP4: Implement "Controls"
    TRM-F SCP5: Assess "Controls"
    TRM-F SCP6: Authorize "Systems"
    TRM-F SCP7: Monitor "Controls"
    ---
"""
def analyze_results(results: List[Dict[str, str]]) -> Dict[str, int]:                                                                                                                         
    analysis = {                                                                                                                                                                              
        "Compliant": 0,                                                                                                                                                                       
        "Non-Compliant": 0,                                                                                                                                                                   
        "Insufficient Information": 0,                                                                                                                                                        
        "Partially Compliant": 0,                                                                                                                                                             
        "Total": len(results)                                                                                                                                                                 
    }                                                                                                                                                                                         
                                                                                                                                                                                              
    for r in results:                                                                                                                                                                         
        status = r["compliance_status"]                                                                                                                                                       
        if status in analysis:                                                                                                                                                                
            analysis[status] += 1                                                                                                                                                             
                                                                                                                                                                                              
    return analysis 

def expand_topic_with_mistral(topic: str) -> str:                                                                                                                                              
    expansion_prompt = f"""                                                                                                                                                                   
    You are a professional compliance auditor. Your task is to convert a compliance checklist item into a clear, expanded technical question to be used to search in the company documents. The Expanded query should be specific and to the point without unnecessary details. It should focus on the key aspects of the checklist item and be suitable for searching in a document database.                                                                                                                                                                                     
                                                                                                                                                                                              
    **Checklist item:** "{topic}"                                                                                                                                                             
                                                                                                                                                                                              
    Before you begin, here are reference terms you may encounter in the checklist item. Use their meanings to inform and clarify your expanded question:                                      
                                                                                                                                                                                              
    * **ITG-F**: IT Governance Framework                                                                                                                                                      
    * **ITSM**: Information Technology Service Management                                                                                                                                     
    * **LP**: Lifecycle Process                                                                                                                                                               
    * **SP**: Supporting Process                                                                                                                                                              
    * **TRM-F**: Technology Risk Management Framework                                                                                                                                         
    * **LRP**: Lifecycle Risk Process                                                                                                                                                         
    * **SCP**: System & Control Process                                                                                                                                                       
    * **CSM-F**: Cyber Security Management Framework                                                                                                                                          
    * **CSP**: Cyber Security Process                                                                                                                                                         
    * **PP**: Process

    You Can also check this additional context which can help you expanding the query for a specific topic: {CONTEXT}                                                                                                                                                                         
                                                                                                                                                                                              
    NOTE: Do not include relationships or alignments with other frameworks unless explicitly mentioned in the original checklist item. The Expanded Query should be direct and to the point and consists of only one question not multiple questions.                                                                                                                                     
                                                                                                                                                                                              
    **Expanded question:**"""                                                                                                                                                                 
                                                                                                                                                                                              
    response = mistral_client.chat(                                                                                                                                                                                        
        model=os.getenv("MISTRAL_MODEL"),                                                                                                                                                                                                        
        messages=[                                                                                                                                                                                                                            
            {"role": "system", "content": "You are a helpful assistant."},                                                                                                                                                                    
            {"role": "user", "content": prompt}                                                                                                                                                              
        ],
        max_tokens=500                                                                                                                                                                                                                                    
    )                                                                                                                                                                                                                                         
    return response.choices[0].message.content                                                                                                                                        
                                                                                                                                                                                              
def retrieve_documents(query: str, company_name: str, top_k: int = 10) -> List[Dict]:                                                                                                                             
    # Generate embedding for the query                                                                                                                                                        
    response = mistral_client.embeddings(                                                                                                                                                     
        model="mistral-embed",                                                                                                                                                                
        input=[query]                                                                                                                                                                         
    )                                                                                                                                                                                         
    query_embedding = response.data[0].embedding                                                                                                                                               
                                                                                                                                                                                              
    # Retrieve documents from Pinecone                                                                                                                                                        
    results = index.query(                                                                                                                                                                
        vector=query_embedding,                                                                                                                                                               
        top_k=top_k,                                                                                                                                                                          
        include_metadata=True,
        namespace=company_name                                                                                                                                                               
    )                                                                                                                                                                                         
                                                                                                                                                                                              
    return results['matches']                                                                                                                                                                 
                                                                                                                                                                                              
def generate_answer(query: str, documents: List[Dict]) -> str:                                                                                                                                                                                
    context = "\n".join([doc['metadata']['text'] for doc in documents])                                                                                                                                                                       
                                                                                                                                                                                                                                              
    if not context:                                                                                                                                                                                                                           
        return "No relevant documents found to answer the question."                                                                                                                                                                          
                                                                                                                                                                                                                                              
    prompt = f"""                                                                                                                                                                                                                             
    You are a knowledgeable and professional assistant. Use the provided context to accurately answer questions related to the company.                                                                                                       
    - Answer the question directly using the available context you have.                                                                                                                                                                      
    - Keep the response concise and to the point.                                                                                                                                                                                             
    - Always return a complete, well-structured sentence.                                                                                                                                                                                     
    - Return answers that are direct and confident.                                                                                                                                                                                           
    - Do not Make up information or provide speculative answers using data outside the provided context.    
    - You should answer the query using the context you have access to, DO NOT ask for any other data/information as this is the only data you can use which is the context provided.                                                                                                                                  
                                                                                                                                                                                                                                              
    Context:                                                                                                                                                                                                                                  
    {context}                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                              
    Question:                                                                                                                                                                                                                                 
    {query}                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                              
    Answer:                                                                                                                                                                                                                                   
    """                                                                                                                                                                                                                                       
                                                                                                                                                                                                                                              
    response = mistral_client.chat(                                                                                                                                                                                        
        model=os.getenv("MISTRAL_MODEL"),                                                                                                                                                                                                     
        messages=[                                                                                                                                                                                                                            
            {"role": "system", "content": "You are a helpful assistant."},                                                                                                                                                                    
            {"role": "user", "content": prompt}                                                                                                                           
        ],
        max_tokens=500                                                                                                                                                                                                                               
    )                                                                                                                                                                                                                                         
    return response.choices[0].message.content                                                                                                                                                                                                
                                                                                                                                                                                                                                              
def generate_answer_for_chat(query: str, documents: List[Dict], results: str) -> str:                                                                                                                                                         
    context = "\n".join([doc['metadata']['text'] for doc in documents])                                                                                                                                                                       
                                                                                                                                                                                                                                              
    if not context:                                                                                                                                                                                                                           
        return "No relevant documents found to answer the question."                                                                                                                                                                          
                                                                                                                                                                                                                                              
    prompt = f"""                                                                                                                                                                                                                             
    You are a knowledgeable and professional assistant. Use the provided context to accurately answer questions related to the company.                                                                                                       
    - Answer the question directly using the available context you have.                                                                                                                                                                      
    - Keep the response concise and to the point.                                                                                                                                                                                             
    - Always return a complete, well-structured sentence.                                                                                                                                                                                     
    - Return answers that are direct and confident.                                                                                                                                                                                           
    - Do not Make up information or provide speculative answers using data outside the provided context.                                                                                                                                      
                                                                                                                                                                                                                                              
    Compliance Evaluation Context If asked about:                                                                                                                                                                                             
    {results}                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                              
    Context:                                                                                                                                                                                                                                  
    {context}                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                              
    Question:                                                                                                                                                                                                                                 
    {query}                                                                                                                                                                                                                                   
                                                                                                                                                                                                                                              
    Answer:                                                                                                                                                                                                                                   
    """                                                                                                                                                                                                                                       
                                                                                                                                                                                                                                              
    response = mistral_client.chat(                                                                                                                                                                                        
        model=os.getenv("MISTRAL_MODEL"),                                                                                                                                                                                                     
        messages=[                                                                                                                                                                                                                            
            {"role": "system", "content": "You are a helpful assistant."},                                                                                                                                                                    
            {"role": "user", "content": prompt}                                                                                                                
        ],
        max_tokens=500                                                                                                                                                                                                                      
    )                                                                                                                                                                                                                                         
    return response.choices[0].message.content

def evaluate_compliance_with_mistral(original_requirement: str, expanded_query: str, answer: str, documents: List[Dict]) -> Dict[str, str]:                                                                                                   
    context = "\n".join([doc['metadata']['text'] for doc in documents])                                                                                                                                                                       
                                                                                                                                                                                                                                              
    if not context:                                                                                                                                                                                                                           
        context = "No relevant documents found to answer the question."                                                                                                                                                                       
                                                                                                                                                                                                                                              
    compliance_prompt = f"""                                                                                                                                                                                                                  
    You are an expert compliance auditor with extensive experience in regulatory assessments. Your task is to evaluate whether a company's documented practices meet a specific compliance requirement.                                       
                                                                                                                                                                                                                                              
    Use the retrieved database evidence in the context provided as your primary source for compliance evaluation. Cross-reference this evidence with the provided answer rather than relying on the answer alone:                             
    {context}                                                                                                                                                                                                                                 
    ---                                                                                                                                                                                                                                       
    COMPLIANCE REQUIREMENT: {original_requirement}                                                                                                                                                                                            
    ---                                                                                                                                                                                                                                       
    DETAILED QUESTION: {expanded_query}                                                                                                                                                                                                       
    ---                                                                                                                                                                                                                                       
    COMPANY'S DOCUMENTED ANSWER: {answer}                                                                                                                                                                                                     
    ---                                                                                                                                                                                                                                       
    Digital Financial Technology Regulations - Legal Framework to use only If Needed:                                                                                                                                                         
    {CONTEXT}                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                              
    ---                                                                                                                                                                                                                                       
    EVALUATION CRITERIA:                                                                                                                                                                                                                      
    - Focus on factual evidence provided in the company's answer                                                                                                                                                                              
    - Consider completeness, specificity, and relevance of the response                                                                                                                                                                       
    - Identify gaps between what is required and what is documented                                                                                                                                                                           
    - If there is no in-depth evidence/implementation/documentation in the answer, **these in-depth evidences** can be submitted later upon request so far now this can be **Compliant** Normally.                                            
                                                                                                                                                                                                                                              
    COMPLIANCE STATUS OPTIONS - Choose ONE:                                                                                                                                                                                                   
    - "Compliant": The answer provides sufficient response to the requirement.                                                                                                                                                                
    - "Non-Compliant": The answer explicitly states the requirement is not met, contradicts the requirement, or contains clear evidence of non-compliance                                                                                     
    - "Insufficient Information": The answer lacks important and must-exist details to determine compliance status.                                                                                                                           
    - "Partially Compliant": The answer didn't meets the important aspects of the requirement, with specific gaps clearly identified.                                                                                                         
                                                                                                                                                                                                                                              
    CONFIDENCE LEVEL Guidelines:                                                                                                                                                                                                              
    - High: Clear, unambiguous evidence supports the assessment OR Evidence is present but could be more detailed or specific.                                                                                                                
    - Low: Assessment is based on limited or unclear information                                                                                                                                                                              
                                                                                                                                                                                                                                              
    Please analyze the answer and provide the response in JSON format with the following structure:   
    JSON Structure: DO NOT EVER ADD JSON TAGS IN YOUR RESPONSE, JUST RETURN THE JSON OBJECT DIRECTLY WITHOUT ANY ADDITIONAL TEXT OR FORMATTING.                                                                                                                                        
    {{                                                                                                                                                                                                                                        
        "status": "Compliant/Non-Compliant/Insufficient Information/Partially Compliant",                                                                                                                                                     
        "confidence": "High/Low",                                                                                                                                                                                                             
        "reasoning": "Brief explanation of your assessment focusing on what evidence supports your conclusion (2-3 sentences max)",                                                                                                           
        "recommendations": "If Compliant: 'None required' or minor suggestions for improvement. If Non-Compliant: Specific actions needed to achieve compliance. If Insufficient Information: What additional documentation/evidence is needed. If Partially Compliant: Actions needed to address identified gaps" # This should be a single string with no newlines or bullet points discussing the recommendation needed to be applied.                                                                                                                                                                    
    }}                                                                                                                                                                                                                                        
    """                                                                                                                                                                                                                                       
                                                                                                                                                                                                                                              
    response = mistral_client.chat(                                                                                                                                                                                                           
        model=os.getenv("MISTRAL_MODEL"),                                                                                                                                                                                                     
        messages=[                                                                                                                                                                                                                            
            {"role": "system", "content": "You are a helpful assistant."},                                                                                                                                                                    
            {"role": "user", "content": compliance_prompt}                                                                                                                                                                                    
        ],                                                                                                                                                                                                                                    
        max_tokens=500                                                                                                                                                                                                                        
    )                                                                                                                                                                                                                                         
                                                                                                                                                                                                                                              
    # Parse the response                                                                                                                                                                                                                      
    result = response.choices[0].message.content                                                                                                                                                                                              
                                                                                                                                                                                                                                              
    # Extract JSON content from code blocks if present                                                                                                                                                                                        
    if result.startswith("```json") and result.endswith("```"):                                                                                                                                                                               
        result = result[7:-3].strip()                                                                                                                                                                                                         
                                                                                                                                                                                                                                              
    # Extract structured information                                                                                                                                                                                                          
    try:                                                                                                                                                                                                                                      
        parsed_result = json.loads(result)                                                                                                                                                                                                    
    except json.JSONDecodeError:                                                                                                                                                                                                              
        parsed_result = {                                                                                                                                                                                                                     
            "status": "Unknown",                                                                                                                                                                                                              
            "confidence": "Unknown",                                                                                                                                                                                                          
            "reasoning": "Unable to parse response",                                                                                                                                                                                          
            "recommendations": "Unable to parse response"                                                                                                                                                                                     
        }                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                              
    return parsed_result                                                                                                                                                                                       
                                                                                                                                                                                              
def process_excel_and_evaluate(filepath: str, company_name: str, save_expanded_queries: bool = True, csv_output_path: str = None) -> List[Dict[str, str]]:
    """
    Process Excel file and optionally save expanded queries to CSV
    
    Args:
        filepath: Path to input CSV file
        company_name: Name of the company
        save_expanded_queries: Whether to save expanded queries to CSV (default: True)
        csv_output_path: Custom path for CSV output (optional)
    """
    df = pd.read_csv(filepath)
    results = []
    expanded_queries_data = []  # Store data for CSV export
    
    for _, row in df.iterrows():
        topic = row["original_description"]  
        # identify = row["IDENTIFY "]            
        # results_guide = row["Results_Guide"]   
        query = row["expanded_query"]
        
        # Skip if Results_Guide is null or empty
        # if pd.isna(results_guide) or results_guide.strip() == "":
        #     print(f"Skipping topic '{topic}' because Results_Guide is null or empty.")
        #     continue
        
        # Concatenate Description and IDENTIFY columns
        # combined_topic = f"{topic} {identify}"
        
        # expanded_query = expand_topic_with_mistral(combined_topic)
        
        print("=============")
        print("Topic: ", topic)
        print("Expanded Query: ", query)
        
        documents = retrieve_documents(query, company_name)
        answer = generate_answer(query, documents)
        
        print("Answer: ", answer)
        
        
        compliance_evaluation = evaluate_compliance_with_mistral(
            original_requirement=topic,
            expanded_query=query,
            answer=answer,
            documents=documents
        )

        print("Status: ", compliance_evaluation["status"])
        print("=============")
        
        # Store data for CSV export
        # expanded_queries_data.append({
        #     "original_description": topic,
        #     "identify": identify,
        #     "combined_topic": combined_topic,
        #     "expanded_query": expanded_query,
        #     "results_guide": results_guide,
        #     "compliance_status": compliance_evaluation["status"],
        #     "confidence_level": compliance_evaluation["confidence"]
        # })
        
        results.append({
            "original_description": topic,
            "expanded_query": query,
            "compliance_status": compliance_evaluation["status"],
            "confidence_level": compliance_evaluation["confidence"],
            "compliance_reasoning": compliance_evaluation["reasoning"],
            "recommendations": compliance_evaluation["recommendations"],
            "answer": answer,
            "references": documents
        })
    
    # Save expanded queries to CSV if requested
    # if save_expanded_queries and expanded_queries_data:
    #     if csv_output_path is None:
    #         # Generate default filename
    #         csv_output_path = f"expanded_queries_Baselines_{company_name}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
    #     expanded_queries_df = pd.DataFrame(expanded_queries_data)
    #     expanded_queries_df.to_csv(csv_output_path, index=False)
    #     print(f"Expanded queries saved to: {csv_output_path}")
    
    return results                                  

def answer_question(query: str, company_name: str, results: str) -> str:
    documents = retrieve_documents(query, company_name)                                                                                                                                        
    answer = generate_answer_for_chat(query, documents, results)

    return answer

def save_results_to_csv(results: List[Dict[str, str]], output_path: str):                                                                                                                     
    flattened_results = []                                                                                                                                                                    
    for r in results:                                                                                                                                                                         
        flat_result = r.copy()                                                                                                                                                                
        flat_result["references"] = "; ".join([f"{ref['id']}" for ref in r["references"]])                                                                                                    
        flat_result["Score"] = 1 if flat_result["compliance_status"] == "Compliant" or flat_result["compliance_status"] == "Partially Compliant" else 0                                                                                                                                                             
        flattened_results.append(flat_result)                                                                                                                                                 
                                                                                                                                                                                              
    df = pd.DataFrame(flattened_results)                                                                                                                                                      
    df.to_csv(output_path, index=False)                                                                                                                                                       
                                                                                                                                                                                              
def main():                                                                                                                                                                                   
    # input_file = "/home/abeltagy/Optomatica/FRA_Project/ThirdSheet.csv"                                                                                                                       
    # output_file = "/home/abeltagy/Optomatica/FRA_Project/ThirdSheet_Results.csv"                                                                                                              
                                                                                                                                                                                              
    # print("Processing compliance evaluation with OpenAI...")                                                                                                                                  
    # results = process_excel_and_evaluate(input_file)                                                                                                                                          
                                                                                                                                                                                              
    # print("Saving results to CSV...")                                                                                                                                                         
    # save_results_to_csv(results, output_file)                                                                                                                                                 
                                                                                                                                                                                              
    # print("\nDetailed Results:")                                                                                                                                                              
    # print("="*80)                                                                                                                                                                             
                                                                                                                                                                                              
    # for r in results:                                                                                                                                                                         
    #     print(f"\n📋 REQUIREMENT: {r['original_description']}")                                                                                                                               
    #     print(f"🔍 Expanded Query: {r['expanded_query']}")                                                                                                                                    
    #     print(f"✅ Status: {r['compliance_status']} (Confidence: {r['confidence_level']})")                                                                                                   
    #     print(f"💭 Reasoning: {r['compliance_reasoning']}")                                                                                                                                   
    #     if r['recommendations'] != "None":                                                                                                                                                    
    #         print(f"💡 Recommendations: {r['recommendations']}")                                                                                                                              
    #     print(f"📄 Answer: {r['answer']}")                                                                                                                                                    
    #     print(f"📚 References: {r['references']}")                                                                                                                                            
    #     print("-" * 80)                                                                                                                                                                       
                                                                                                                                                                                              
    # # Add the analysis                                                                                                                                                                        
    # analysis = analyze_results(results)                                                                                                                                                       
    # print("\nCompliance Analysis:")                                                                                                                                                           
    # print("="*80)                                                                                                                                                                             
    # print(f"Total Requirements: {analysis['Total']}")                                                                                                                                         
    # print(f"Compliant: {analysis['Compliant']}")                                                                                                                                              
    # print(f"Non-Compliant: {analysis['Non-Compliant']}")                                                                                                                                      
    # print(f"Insufficient Information: {analysis['Insufficient Information']}")                                                                                                                
    # print(f"Partially Compliant: {analysis['Partially Compliant']}")                                                                                                                          
    # print("="*80)

    answer = answer_question(" data protection policies?", "optomatica")
    print("Answer to the question:", answer)

if __name__ == "__main__":                                                                                                                                                                    
    main()                                  