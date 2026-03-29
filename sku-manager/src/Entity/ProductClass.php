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
use Symfony\Component\Validator\Constraints as Assert;

/**
 * @ORM\Entity(repositoryClass="App\Repository\ProductClassRepository")
 *
 * @Serializer\ExclusionPolicy("ALL")
 */
class ProductClass extends AbstractEntity
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
     * @ORM\Column(type="string", length=255)
     *
     * @Serializer\Expose()
     * @Serializer\Groups({"list", "details"})
     *
     * @Assert\NotBlank()
     */
    private string $name = '';

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
     * @ORM\ManyToOne(targetEntity="App\Entity\System", inversedBy="productClasses")
     * @ORM\JoinColumn(nullable=false)
     *
     * @Assert\NotBlank()
     */
    private System $system;

    /**
     * @ORM\ManyToOne(targetEntity="App\Entity\ProductClass")
     *
     * @Serializer\Expose()
     * @Serializer\Groups({"details"})
     */
    private ?ProductClass $parentClass = null;

    /**
     * @ORM\ManyToMany(targetEntity="App\Entity\Product", mappedBy="productClasses")
     *
     * @Serializer\Expose()
     * @Serializer\Groups({"details"})
     */
    private Collection $products;

    public function __construct()
    {
        $this->products = new ArrayCollection();
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
     * @return ProductClass|null
     */
    public function getParentClass(): ?ProductClass
    {
        return $this->parentClass;
    }

    /**
     * @param ProductClass|null $parentClass
     *
     * @return $this
     */
    public function setParentClass(?self $parentClass): self
    {
        $this->parentClass = $parentClass;

        return $this;
    }

    /**
     * @Serializer\VirtualProperty
     * @Serializer\Type("int")
     * @Serializer\Groups({"list", "details"})
     *
     * @return int|null
     */
    public function getParentClassId(): ?int
    {
        return $this->getParentClass() ? $this->getParentClass()->getId() : null;
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
     * @return Collection|Product[]
     */
    public function getProducts(): Collection
    {
        return $this->products;
    }

    public function addProduct(Product $product): self
    {
        if (!$this->products->contains($product)) {
            $this->products[] = $product;
            $product->addProductClass($this);
        }

        return $this;
    }

    public function removeProduct(Product $product): self
    {
        if ($this->products->contains($product)) {
            $this->products->removeElement($product);
            $product->removeProductClass($this);
        }

        return $this;
    }
}
