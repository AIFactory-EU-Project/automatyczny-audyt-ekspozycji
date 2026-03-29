<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Entity;

use DateTimeInterface;
use Doctrine\Common\Collections\ArrayCollection;
use Doctrine\Common\Collections\Collection;
use Doctrine\ORM\Mapping as ORM;
use JMS\Serializer\Annotation as Serializer;
use Swagger\Annotations as SWG;
use Symfony\Component\Validator\Constraints as Assert;

/**
 * @ORM\Entity(repositoryClass="App\Repository\ProductGroupRepository")
 *
 * @Serializer\ExclusionPolicy("ALL")
 */
class ProductGroup extends AbstractEntity
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
     * @ORM\OneToMany(targetEntity="App\Entity\Training", mappedBy="productGroup")
     */
    private Collection $trainings;

    /**
     * @ORM\ManyToOne(targetEntity="App\Entity\System", inversedBy="productGroups")
     * @ORM\JoinColumn(nullable=false)
     *
     * @Serializer\Exclude()
     *
     * @Assert\NotBlank()
     */
    private System $system;

    /**
     * @ORM\ManyToMany(targetEntity="App\Entity\Product", inversedBy="productGroups")
     *
     * @Serializer\Expose()
     * @Serializer\Groups({"details"})
     */
    private Collection $products;

    /**
     * @ORM\Column(type="string", length=255)
     *
     * @Serializer\Expose()
     * @Serializer\Groups({"list", "details"})
     *
     * @Assert\NotBlank()
     */
    private ?string $name = null;

    /**
     * @ORM\Column(type="string", length=512)
     *
     * @Serializer\Expose()
     * @Serializer\Groups({"list", "details"})
     *
     * @Assert\NotBlank()
     */
    private ?string $description = null;

    /**
     * @ORM\Column(type="boolean")
     */
    private bool $availableOffline = false;

    /**
     * @ORM\Column(type="boolean")
     */
    private bool $availableOnline = false;

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
     * @ORM\Column(type="integer")
     *
     * @Serializer\Expose()
     * @Serializer\Groups({"list", "details"})
     */
    private int $trainingStatus = 0;

    /**
     * ProductGroup constructor.
     */
    public function __construct()
    {
        $this->trainings = new ArrayCollection();
        $this->products = new ArrayCollection();
    }

    /**
     * @return Collection|Training[]
     */
    public function getTrainings(): Collection
    {
        return $this->trainings;
    }

    /**
     * @param Training $training
     *
     * @return $this
     */
    public function addTraining(Training $training): self
    {
        if (!$this->trainings->contains($training)) {
            $this->trainings[] = $training;
            $training->setProductGroup($this);
        }

        return $this;
    }

    /**
     * @param Training $training
     *
     * @return $this
     */
    public function removeTraining(Training $training): self
    {
        if ($this->trainings->contains($training)) {
            $this->trainings->removeElement($training);
            // set the owning side to null (unless already changed)
            if ($training->getProductGroup() === $this) {
                $training->setProductGroup(null);
            }
        }

        return $this;
    }

    /**
     * @return System
     */
    public function getSystem(): System
    {
        return $this->system;
    }

    /**
     * @param System $system
     *
     * @return $this
     */
    public function setSystem(System $system): self
    {
        $this->system = $system;

        return $this;
    }

    /**
     * @return Collection|Product[]
     */
    public function getProducts(): Collection
    {
        return $this->products;
    }

    /**
     * @param Product $product
     *
     * @return $this
     */
    public function addProduct(Product $product): self
    {
        if (!$this->products->contains($product)) {
            $this->products[] = $product;
        }

        return $this;
    }

    /**
     * @param Product $product
     *
     * @return $this
     */
    public function removeProduct(Product $product): self
    {
        if ($this->products->contains($product)) {
            $this->products->removeElement($product);
        }

        return $this;
    }

    /**
     * @return string
     */
    public function getName(): ?string
    {
        return $this->name;
    }

    /**
     * @param string $name
     *
     * @return $this
     */
    public function setName(string $name): self
    {
        $this->name = $name;

        return $this;
    }

    public function getDescription(): ?string
    {
        return $this->description;
    }

    /**
     * @param string $description
     *
     * @return $this
     */
    public function setDescription(string $description): self
    {
        $this->description = $description;

        return $this;
    }

    /**
     * @return bool
     */
    public function getAvailableOffline(): bool
    {
        return $this->availableOffline;
    }

    /**
     * @param bool $availableOffline
     *
     * @return $this
     */
    public function setAvailableOffline(bool $availableOffline): self
    {
        $this->availableOffline = $availableOffline;

        return $this;
    }

    /**
     * @return bool
     */
    public function getAvailableOnline(): bool
    {
        return $this->availableOnline;
    }

    /**
     * @param bool $availableOnline
     *
     * @return $this
     */
    public function setAvailableOnline(bool $availableOnline): self
    {
        $this->availableOnline = $availableOnline;

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
     * @return int
     */
    public function getTrainingStatus(): int
    {
        return $this->trainingStatus;
    }

    /**
     * @param int $trainingStatus
     *
     * @return $this
     */
    public function setTrainingStatus(int $trainingStatus): self
    {
        $this->trainingStatus = $trainingStatus;

        return $this;
    }
}
