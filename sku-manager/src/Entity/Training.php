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
 * @ORM\Entity(repositoryClass="App\Repository\TrainingRepository")
 *
 * @Serializer\ExclusionPolicy("ALL")
 */
class Training extends AbstractEntity
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
     * @ORM\ManyToOne(targetEntity="App\Entity\ProductGroup", inversedBy="s")
     * @ORM\JoinColumn(nullable=false)
     *
     * @Assert\NotBlank()
     */
    private ProductGroup $productGroup;

    /**
     * @ORM\Column(type="integer")
     *
     * @Serializer\Expose()
     * @Serializer\Groups({"list", "details"})
     *
     * @Assert\NotBlank()
     */
    private int $status;

    /**
     * @ORM\Column(type="integer")
     *
     * @Serializer\Expose()
     * @Serializer\Groups({"list", "details"})
     *
     * @Assert\NotBlank()
     */
    private int $stale;

    /**
     * @ORM\Column(type="string", length=255)
     *
     * @Serializer\Expose()
     * @Serializer\Groups({"list", "details"})
     */
    private ?string $hash;

    /**
     * @ORM\Column(type="json")
     *
     * @SWG\Property(type="Object")
     *
     * @Assert\NotBlank()
     */
    private array $dataSnapshot = [];

    /**
     * @ORM\Column(type="datetime", nullable=true)
     */
    private ?DateTimeInterface $startDate;

    /**
     * @ORM\Column(type="datetime")
     */
    private ?DateTimeInterface $scheduledStartDate;

    /**
     * @ORM\Column(type="datetime", nullable=true)
     */
    private ?DateTimeInterface $endDate;

    /**
     * @ORM\Column(type="datetime", nullable=true)
     */
    private ?DateTimeInterface $estimatedEndDate;

    /**
     * @ORM\Column(type="string", length=255, nullable=true)
     */
    private ?string $fileLocation;

    /**
     * @return ProductGroup
     */
    public function getProductGroup(): ProductGroup
    {
        return $this->productGroup;
    }

    /**
     * @param ProductGroup $productGroup
     *
     * @return $this
     */
    public function setProductGroup(ProductGroup $productGroup): self
    {
        $this->productGroup = $productGroup;

        return $this;
    }

    /**
     * @return int
     */
    public function getStatus(): int
    {
        return $this->status;
    }

    /**
     * @param int $status
     *
     * @return $this
     */
    public function setStatus(int $status): self
    {
        $this->status = $status;

        return $this;
    }

    /**
     * @return int
     */
    public function getStale(): int
    {
        return $this->stale;
    }

    /**
     * @param int $stale
     *
     * @return $this
     */
    public function setStale(int $stale): self
    {
        $this->stale = $stale;

        return $this;
    }

    /**
     * @return string|null
     */
    public function getHash(): ?string
    {
        return $this->hash;
    }

    /**
     * @param string $hash
     *
     * @return $this
     */
    public function setHash(string $hash): self
    {
        $this->hash = $hash;

        return $this;
    }

    /**
     * @return array|null
     */
    public function getDataSnapshot(): ?array
    {
        return $this->dataSnapshot;
    }

    /**
     * @param array $dataSnapshot
     *
     * @return $this
     */
    public function setDataSnapshot(array $dataSnapshot): self
    {
        $this->dataSnapshot = $dataSnapshot;

        return $this;
    }

    /**
     * @return DateTimeInterface|null
     */
    public function getStartDate(): ?DateTimeInterface
    {
        return $this->startDate;
    }

    /**
     * @param DateTimeInterface|null $startDate
     *
     * @return $this
     */
    public function setStartDate(?DateTimeInterface $startDate): self
    {
        $this->startDate = $startDate;

        return $this;
    }

    /**
     * @return DateTimeInterface|null
     */
    public function getScheduledStartDate(): ?DateTimeInterface
    {
        return $this->scheduledStartDate;
    }

    /**
     * @param DateTimeInterface $scheduledStartDate
     *
     * @return $this
     */
    public function setScheduledStartDate(DateTimeInterface $scheduledStartDate): self
    {
        $this->scheduledStartDate = $scheduledStartDate;

        return $this;
    }

    /**
     * @return DateTimeInterface|null
     */
    public function getEndDate(): ?DateTimeInterface
    {
        return $this->endDate;
    }

    /**
     * @param DateTimeInterface|null $endDate
     *
     * @return $this
     */
    public function setEndDate(?DateTimeInterface $endDate): self
    {
        $this->endDate = $endDate;

        return $this;
    }

    /**
     * @return DateTimeInterface|null
     */
    public function getEstimatedEndDate(): ?DateTimeInterface
    {
        return $this->estimatedEndDate;
    }

    /**
     * @param DateTimeInterface|null $estimatedEndDate
     *
     * @return $this
     */
    public function setEstimatedEndDate(?DateTimeInterface $estimatedEndDate): self
    {
        $this->estimatedEndDate = $estimatedEndDate;

        return $this;
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
     * @Serializer\VirtualProperty
     * @Serializer\Type("int")
     * @Serializer\Groups({"list", "details"})
     *
     * @return int|null
     */
    public function getProductGroupId(): ?int
    {
        return $this->getProductGroup() ? $this->getProductGroup()->getId() : null;
    }
}
