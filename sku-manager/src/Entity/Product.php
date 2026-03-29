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
use Symfony\Bridge\Doctrine\Validator\Constraints\UniqueEntity;
use Symfony\Component\Validator\Constraints as Assert;
use Symfony\Component\Validator\GroupSequenceProviderInterface;

/**
 * @ORM\Entity(repositoryClass="App\Repository\ProductRepository")
 *
 * @Assert\GroupSequenceProvider()
 *
 * @UniqueEntity(fields={"active", "system", "name"}, errorPath="name", groups={"active"})
 * @UniqueEntity(fields={"active", "system", "clientId"}, errorPath="clientId", groups={"active"})
 *
 * @Serializer\ExclusionPolicy("ALL")
 */
class Product extends AbstractEntity implements GroupSequenceProviderInterface
{
    public function getGroupSequence()
    {
        return [
            [
                'Product',
                $this->active ? 'active' : 'inactive',
            ],
        ];
    }

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
     * @ORM\ManyToOne(targetEntity="App\Entity\System", inversedBy="products")
     * @ORM\JoinColumn(nullable=false)
     *
     * @Assert\NotBlank()
     */
    private System $system;

    /**
     * @ORM\ManyToMany(targetEntity="App\Entity\ProductGroup", mappedBy="products")
     *
     * @Serializer\Expose()
     * @Serializer\Groups({"details"})
     */
    private Collection $productGroups;

    /**
     * @ORM\OneToMany(targetEntity="App\Entity\Image", mappedBy="product")
     *
     * @Serializer\Expose()
     * @Serializer\Groups({"details"})
     */
    private Collection $images;

    /**
     * @ORM\Column(type="string", length=255)
     *
     * @Serializer\Expose()
     * @Serializer\Groups({"list", "details"})
     *
     * @Assert\NotBlank()
     */
    private string $name = '';

    /**
     * @ORM\Column(type="string", length=512)
     *
     * @Serializer\Expose()
     * @Serializer\Groups({"list", "details"})
     *
     * @Assert\NotBlank()
     */
    private string $tags = '';

    /**
     * @ORM\Column(type="json")
     *
     * @Serializer\Expose()
     * @Serializer\Groups({"list", "details"})
     *
     * @SWG\Property(type="Object")
     */
    private array $additionalMeta = [];

    /**
     * @ORM\Column(type="string", length=128)
     *
     * @Serializer\Expose()
     * @Serializer\Groups({"list", "details"})
     *
     * @Assert\NotBlank()
     */
    private string $clientId = '';

    /**
     * @ORM\ManyToOne(targetEntity="App\Entity\Player", inversedBy="products")
     *
     * @Serializer\Expose()
     * @Serializer\Groups({"list", "details"})
     *
     * @Assert\NotBlank()
     */
    private ?Player $player = null;

    /**
     * @ORM\ManyToMany(targetEntity="App\Entity\ProductClass", inversedBy="products")
     *
     * @Serializer\Expose()
     * @Serializer\Groups({"details"})
     */
    private Collection $productClasses;

    /**
     * @ORM\ManyToOne(targetEntity="App\Entity\Brand", inversedBy="products")
     *
     * @Serializer\Expose()
     * @Serializer\Groups({"list", "details"})
     *
     * @Assert\NotBlank()
     */
    private ?Brand $brand = null;

    /**
     * @ORM\ManyToOne(targetEntity="App\Entity\Category", inversedBy="products")
     *
     * @Serializer\Expose()
     * @Serializer\Groups({"list", "details"})
     *
     * @Assert\NotBlank()
     */
    private ?Category $category = null;

    /**
     * Product constructor.
     */
    public function __construct()
    {
        $this->productGroups = new ArrayCollection();
        $this->images = new ArrayCollection();
        $this->productClasses = new ArrayCollection();
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
    public function setSystem(?System $system): self
    {
        $this->system = $system;

        return $this;
    }

    /**
     * @return Collection|ProductGroup[]
     */
    public function getProductGroups(): Collection
    {
        return $this->productGroups;
    }

    /**
     * @param ProductGroup $productGroup
     *
     * @return $this
     */
    public function addProductGroup(ProductGroup $productGroup): self
    {
        if (!$this->productGroups->contains($productGroup)) {
            $this->productGroups[] = $productGroup;
            $productGroup->addProduct($this);
        }

        return $this;
    }

    /**
     * @param ProductGroup $productGroup
     *
     * @return $this
     */
    public function removeProductGroup(ProductGroup $productGroup): self
    {
        if ($this->productGroups->contains($productGroup)) {
            $this->productGroups->removeElement($productGroup);
            $productGroup->removeProduct($this);
        }

        return $this;
    }

    /**
     * @return Collection|Image[]
     */
    public function getImages(): Collection
    {
        return $this->images;
    }

    /**
     * @param Image $image
     *
     * @return $this
     */
    public function addImage(Image $image): self
    {
        if (!$this->images->contains($image)) {
            $this->images[] = $image;
            $image->setProduct($this);
        }

        return $this;
    }

    /**
     * @param Image $image
     *
     * @return $this
     */
    public function removeImage(Image $image): self
    {
        if ($this->images->contains($image)) {
            $this->images->removeElement($image);
            // set the owning side to null (unless already changed)
            if ($image->getProduct() === $this) {
                $image->setProduct(null);
            }
        }

        return $this;
    }

    /**
     * @return string
     */
    public function getName(): string
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
     * @return string
     */
    public function getClientId(): string
    {
        return $this->clientId;
    }

    /**
     * @param string $clientId
     *
     * @return $this
     */
    public function setClientId(string $clientId): self
    {
        $this->clientId = $clientId;

        return $this;
    }

    /**
     * @return Collection|ProductClass[]
     */
    public function getProductClasses(): Collection
    {
        return $this->productClasses;
    }

    /**
     * @param ProductClass $productClass
     *
     * @return $this
     */
    public function addProductClass(ProductClass $productClass): self
    {
        if (!$this->productClasses->contains($productClass)) {
            $this->productClasses[] = $productClass;
        }

        return $this;
    }

    /**
     * @param ProductClass $productClass
     *
     * @return $this
     */
    public function removeProductClass(ProductClass $productClass): self
    {
        if ($this->productClasses->contains($productClass)) {
            $this->productClasses->removeElement($productClass);
        }

        return $this;
    }

    /**
     * @return Brand|null
     */
    public function getBrand(): ?Brand
    {
        return $this->brand;
    }

    /**
     * @param Brand|null $brand
     *
     * @return $this
     */
    public function setBrand(?Brand $brand): self
    {
        $this->brand = $brand;

        return $this;
    }

    /**
     * @return Category|null
     */
    public function getCategory(): ?Category
    {
        return $this->category;
    }

    /**
     * @param Category|null $category
     *
     * @return $this
     */
    public function setCategory(?Category $category): self
    {
        $this->category = $category;

        return $this;
    }

    /**
     * @return Player|null
     */
    public function getPlayer(): ?Player
    {
        return $this->player;
    }

    /**
     * @param Player|null $player
     *
     * @return $this
     */
    public function setPlayer(?Player $player): self
    {
        $this->player = $player;

        return $this;
    }
}
