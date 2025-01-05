from kubernetes import client, config, watch
import requests

# Load kubeconfig
config.load_kube_config()

# Define API clients
v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()


def fetch_website_content(url):
    """Fetch HTML content from the URL."""
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def create_configmap(namespace, name, data):
    """Create a ConfigMap with the HTML content."""
    metadata = client.V1ObjectMeta(name=name)
    body = client.V1ConfigMap(metadata=metadata, data={"index.html": data})
    return v1.create_namespaced_config_map(namespace=namespace, body=body)


def create_deployment(namespace, name):
    """Create a Deployment to serve the website."""
    container = client.V1Container(
        name="nginx",
        image="nginx",
        volume_mounts=[client.V1VolumeMount(
            mount_path="/usr/share/nginx/html",
            name="html-volume"
        )]
    )
    volume = client.V1Volume(
        name="html-volume",
        config_map=client.V1ConfigMapVolumeSource(name=name)
    )
    pod_spec = client.V1PodSpec(containers=[container], volumes=[volume])
    template = client.V1PodTemplateSpec(metadata=client.V1ObjectMeta(
        labels={"app": name}), spec=pod_spec)
    spec = client.V1DeploymentSpec(replicas=1,
                                   selector={"matchLabels": {"app": name}},
                                   template=template)
    deployment = client.V1Deployment(
        metadata=client.V1ObjectMeta(name=name),
        spec=spec)
    return apps_v1.create_namespaced_deployment(
        namespace=namespace,
        body=deployment)


def watch_dummysites():
    """Watch for DummySite resources."""
    custom_api = client.CustomObjectsApi()
    namespace = "default"
    resource_group = "example.com"
    resource_version = "v1"
    resource_plural = "dummysites"

    watcher = watch.Watch()
    for event in watcher.stream(
         custom_api.list_namespaced_custom_object,
         resource_group, resource_version,
         namespace,
         resource_plural):

        resource = event['object']
        event_type = event['type']
        name = resource['metadata']['name']
        spec = resource['spec']
        website_url = spec['website_url']

        print(f"Event: {event_type}, Name: {name}, URL: {website_url}")

        if event_type == "ADDED":
            html_content = fetch_website_content(website_url)
            create_configmap(namespace, name, html_content)
            create_deployment(namespace, name)


if __name__ == "__main__":
    watch_dummysites()
