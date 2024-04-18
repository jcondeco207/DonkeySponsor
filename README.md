## Infrastructure Solution Choice

In this project we want to use a containerized solution, for this sake the possible Google Cloud Platform products that we could use were Kubernetes Engine, VMware Engine and Cloud Run.

One of the most important thing to consider when choosing a cloud service provider and the product to use is the pricing and the scalability. So, for a better choosing we did a deeper analisys of the three products.

### [Kubernetes Engine](!https://cloud.google.com/kubernetes-engine/docs/concepts/kubernetes-engine-overview)

GKE is ideal if you need a platform that lets you configure the infrastructure that runs your containerized apps, such as networking, scaling, hardware, and security. GKE provides the operational power of Kubernetes while managing many of the underlying components, such as the control plane and nodes, for you.

#### Pricing
This service has two editions, the standard edition and the enterprise edition. Because our project is not complex we would choose the standard edition.

This edition is priced at $0.10 per cluster per hour.

### [VMware Engine](!https://cloud.google.com/vmware-engine/docs/overview)

Google Cloud VMware Engine is a fully managed service that lets you run the VMware platform in Google Cloud. VMware Engine provides you with VMware operational continuity so you can benefit from a cloud consumption model and lower your total cost of ownership. VMware Engine also offers on-demand provisioning, pay-as-you-grow, and capacity optimization.

#### Pricing

Pricing is based on consumption and commitment term; options include on-demand or committed use discounts for one- and three-year terms, with a three-node minimum.

For our project this is a very high cost solution. With cost rounding $10.00 per hour.

### [Cloud Run](!https://cloud.google.com/run/docs?_gl=1*1jovx8n*_ga*MTE5ODkxOTA0OC4xNzEyMTgxNzk3*_ga_WH2QY8WWF5*MTcxMzAxNjU4MS4yLjEuMTcxMzAyMzA3My4wLjAuMA..&_ga=2.250502598.-1198919048.1712181797)
Cloud Run is a managed compute platform that enables you to run containers that are invocable via requests or events. Cloud Run is serverless: it abstracts away all infrastructure management, so you can focus on what matters most — building great applications. 

#### Pricing
Cloud Run charges you only for the resources you use, rounded up to the nearest 100 millisecond. Your total Cloud Run bill will be the sum of the resource usage in the pricing table after the free tier is applied.

### Conclusion
Using the Google Cloud Price Estimator we did calculation for all three solutions. Were are the results: 

+ [Kubernetes Engine](/Pricing/kubernetesEnginePricing.csv)
+ [VMware Engine](/Pricing/vmwareEnginePricing.csv)
+ [Cloud Run](/Pricing/cloudRunPricing.csv)

For this WebApp the product that we choose was Cloud Run for the low pricing when comparing with the other products.

## Frontend Pages

+ Login
+ Home Page (Opened to all users)
+ Farm management Page (Opened to produtors)
    + List donkeys
    + Post news of donkey
    + Add donkeys
    + Delete donkeys
+ My sponsored donkeys page (Opened to sponsors)
+ Sponsored news (Opened to sponsors)
