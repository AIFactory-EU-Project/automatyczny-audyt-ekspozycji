<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Entity;

use DateTimeInterface;
use Doctrine\ORM\Mapping as ORM;
use JMS\Serializer\Annotation as Serializer;
use Swagger\Annotations as SWG;
use Symfony\Component\Validator\Constraints as Assert;

/**
 * @ORM\Entity(repositoryClass="App\Repository\ImageRepository")
 *
 * @Serializer\ExclusionPolicy("ALL")
 */
class Image extends AbstractEntity
{
    /**
     * @ORM\Id()
     * @ORM\GeneratedValue()
     * @ORM\Column(type="integer")
     *
     * @Serializer\Expose()
     * @Serializer\Groups({"list", "details"})
     */
    protected ?int $id = null;

    /**
     * @ORM\Column(type="datetime")
     *
     * @Serializer\Expose()
     * @Serializer\Groups({"list", "details"})
     *
     * @Assert\NotBlank()
     */
    protected ?DateTimeInterface $createdDate;

    /**
     * @ORM\Column(type="datetime")
     *
     * @Serializer\Expose()
     * @Serializer\Groups({"list", "details"})
     *
     * @Assert\NotBlank()
     */
    protected ?DateTimeInterface $updatedDate;

    /**
     * @ORM\ManyToOne(targetEntity="App\Entity\Product", inversedBy="images")
     * @ORM\JoinColumn(nullable=false)
     *
     * @Assert\NotBlank()
     */
    private Product $product;

    /**
     * @ORM\Column(type="string", length=1024)
     *
     * @Serializer\Expose()
     * @Serializer\Groups({"list", "details"})
     */
    private string $sourceUrl = '';

    /**
     * @ORM\Column(type="string", length=1024)
     *
     * @Serializer\Expose()
     * @Serializer\Groups({"list", "details"})
     */
    private string $sourceSmallUrl = '';

    /**
     * @ORM\Column(type="string", length=512)
     *
     * @Serializer\Expose()
     * @Serializer\Groups({"list", "details"})
     */
    private string $tags = '';

    /**
     * @ORM\Column(type="json")
     *
     * @SWG\Property(type="Object")
     */
    private array $additionalMeta = [];

    /**
     * @ORM\Column(type="boolean")
     *
     * @Serializer\Expose()
     * @Serializer\Groups({"list", "details"})
     */
    private ?bool $main = false;

    private ?string $content = null;

    /**
     * @ORM\Column(type="string", length=512, nullable=true)
     */
    private ?string $fileLocation = null;

    /**
     * @ORM\Column(type="string", length=512, nullable=true)
     */
    private ?string $fileLocationSmall = null;

    /**
     * @ORM\Column(type="string", length=255, nullable=true)
     */
    private ?string $baseFilename = null;

    /**
     * @return Product
     */
    public function getProduct(): Product
    {
        return $this->product;
    }

    /**
     * @param Product $product
     *
     * @return $this
     */
    public function setProduct(Product $product): self
    {
        $this->product = $product;

        return $this;
    }

    /**
     * @return string
     */
    public function getSourceUrl(): string
    {
        return $this->sourceUrl;
    }

    /**
     * @param string $sourceUrl
     *
     * @return $this
     */
    public function setSourceUrl(string $sourceUrl): self
    {
        $this->sourceUrl = $sourceUrl;

        return $this;
    }

    /**
     * @return string
     */
    public function getSourceSmallUrl(): string
    {
        return $this->sourceSmallUrl;
    }

    /**
     * @param string $sourceSmallUrl
     *
     * @return $this
     */
    public function setSourceSmallUrl(string $sourceSmallUrl): self
    {
        $this->sourceSmallUrl = $sourceSmallUrl;

        return $this;
    }

    /**
     * @return string
     */
    public function getTags(): string
    {
        return $this->tags;
    }

    /**
     * @param string $tags
     *
     * @return $this
     */
    public function setTags(string $tags): self
    {
        $this->tags = $tags;

        return $this;
    }

    /**
     * @return array
     */
    public function getAdditionalMeta(): array
    {
        return $this->additionalMeta;
    }

    /**
     * @param array $additionalMeta
     *
     * @return $this
     */
    public function setAdditionalMeta(array $additionalMeta): self
    {
        $this->additionalMeta = $additionalMeta;

        return $this;
    }

    /**
     * @return int|null
     *
     * @Serializer\VirtualProperty
     * @Serializer\Type("int")
     * @Serializer\Groups({"list", "details"})
     */
    public function getProductId(): ?int
    {
        return $this->getProduct() ? $this->getProduct()->getId() : null;
    }

    /**
     * @return bool|null
     */
    public function getMain(): ?bool
    {
        return $this->main;
    }

    /**
     * @param bool $main
     *
     * @return $this
     */
    public function setMain(bool $main): self
    {
        $this->main = $main;

        return $this;
    }

    /**
     * @return string|null
     */
    public function getContent(): ?string
    {
        return $this->content;
    }

    /**
     * @param string|null $content
     */
    public function setContent(?string $content): void
    {
        $this->content = $content;
    }

    /**
     * @return string|null
     */
    public function getFileLocation(): ?string
    {
        return $this->fileLocation;
    }

    /**
     * @param string|null $fileLocation
     *
     * @return $this
     */
    public function setFileLocation(?string $fileLocation): self
    {
        $this->fileLocation = $fileLocation;

        return $this;
    }

    /**
     * @return string|null
     */
    public function getFileLocationSmall(): ?string
    {
        return $this->fileLocationSmall;
    }

    /**
     * @param string|null $fileLocationSmall
     *
     * @return $this
     */
    public function setFileLocationSmall(?string $fileLocationSmall): self
    {
        $this->fileLocationSmall = $fileLocationSmall;

        return $this;
    }

    /**
     * @return string|null
     */
    public function getBaseFilename(): ?string
    {
        return $this->baseFilename;
    }

    /**
     * @param string|null $baseFilename
     *
     * @return Image
     */
    public function setBaseFilename(?string $baseFilename): Image
    {
        $this->baseFilename = $baseFilename;

        return $this;
    }
}
