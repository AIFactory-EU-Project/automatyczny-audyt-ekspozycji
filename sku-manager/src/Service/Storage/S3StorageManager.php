<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Service\Storage;

use Aws\CloudFront\CloudFrontClient;
use Aws\S3\S3Client;
use DateTime;
use Symfony\Component\DependencyInjection\ParameterBag\ParameterBagInterface;

class S3StorageManager implements StorageManagerInterface
{
    private S3Client $client;

    private CloudFrontClient $cloudFrontClient;

    private string $mediaBucketName;

    private string $nnBucketName;

    private string $mediaCloudFrontUrlPrefix;

    private ParameterBagInterface $bag;

    public function __construct(ParameterBagInterface $bag)
    {
        $this->bag = $bag;
        $this->mediaBucketName = $bag->get('aws_s3_media_bucket_name');
        $this->nnBucketName = $bag->get('aws_s3_nn_bucket_name');

        $this->mediaCloudFrontUrlPrefix = $bag->get('aws_cloudfront_media_url').'/';

        $this->client = new S3Client([
            'version' => 'latest',
            'region' => $bag->get('aws_s3_region'),
            'credentials' => [
                'key' => $bag->get('aws_access_key_id'),
                'secret' => $bag->get('aws_secret_access_key'),
            ],
        ]);

        $this->cloudFrontClient = new CloudFrontClient([
            'version' => 'latest',
            'region' => $bag->get('aws_cloudfront_region'),
            'credentials' => [
                'key' => $this->bag->get('aws_access_key_id'),
                'secret' => $this->bag->get('aws_secret_access_key'),
            ],
        ]);
    }

    public function uploadMediaFile($content, string $destinationPath)
    {
        $this->client->putObject([
            'Bucket' => $this->mediaBucketName,
            'Key' => $destinationPath,
            'Body' => $content,
        ]);
    }

    public function getMediaPublicUrl(string $destinationPath): string
    {
        $resourceKey = $this->mediaCloudFrontUrlPrefix.$destinationPath;
        $url = $this->cloudFrontClient->getSignedUrl([
            'url' => $resourceKey,
            'expires' => date_timestamp_get(new DateTime('2100-01-01')),
            'private_key' => $this->bag->get('aws_cloudfront_media_private_key'),
            'key_pair_id' => $this->bag->get('aws_cloudfront_media_key_pair_id'),
        ]);

        return $url;
    }

    public function getNNPublicUrl(string $destinationPath): string
    {
        $cmd = $this->client->getCommand('GetObject', [
            'Bucket' => $this->nnBucketName,
            'Key' => $destinationPath,
        ]);
        $request = $this->client->createPresignedRequest($cmd, '+24 hours');

        return $presignedUrl = (string) $request->getUri();
    }
}
