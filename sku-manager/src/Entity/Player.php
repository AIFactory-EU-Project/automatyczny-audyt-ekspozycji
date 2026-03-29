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
use Symfony\Bridge\Doctrine\Validator\Constraints\UniqueEntity;
use Symfony\Component\Validator\Constraints as Assert;
use Symfony\Component\Validator\GroupSequenceProviderInterface;

/**
 * @ORM\Entity(repositoryClass="App\Repository\PlayerRepository")
 *
 * @Assert\GroupSequenceProvider()
 *
 * @UniqueEntity(fields={"active", "system", "name"}, errorPath="name", groups={"active"})
 *
 * @Serializer\ExclusionPolicy("ALL")
 */
class Player extends AbstractEntity implements GroupSequenceProviderInterface
{
    public function getGroupSequence()
    {
        return [
            [
                'Player',
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
     * @ORM\Column(type="string", length=255)
     *
     * @Serializer\Expose()
     * @Serializer\Groups({"list", "details"})
     *
     * @Assert\NotBlank()
     */
    private ?string $name = null;

    /**
     * @ORM\ManyToOne(targetEntity="App\Entity\System", inversedBy="players")
     * @ORM\JoinColumn(nullable=false)
     *
     * @Assert\NotBlank()
     */
    private ?System $system;

    /**
     * @ORM\Column(type="boolean")
     *
     * @Serializer\Expose()
     * @Serializer\Groups({"list", "details"})
     */
    private ?bool $competitor = false;

    /**
     * @ORM\OneToMany(targetEntity="App\Entity\Product", mappedBy="player")
     */
    private Collection $products;

    /**
     * Player constructor.
     */
    public function __construct()
    {
        $this->products = new ArrayCollection();
    }

    /**
     * @return int|null
     */
    public function getId(): ?int
    {
        return $this->id;
    }

    /**
     * @return string|null
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

    /**
     * @return System|null
     */
    public function getSystem(): ?System
    {
        return $this->system;
    }

    /**
     * @param System|null $system
     *
     * @return $this
     */
    public function setSystem(?System $system): self
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
            $product->setPlayer($this);
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
            // set the owning side to null (unless already changed)
            if ($product->getPlayer() === $this) {
                $product->setPlayer(null);
            }
        }

        return $this;
    }

    /**
     * @return bool|null
     */
    public function getCompetitor(): ?bool
    {
        return $this->competitor;
    }

    /**
     * @param bool|null $competitor
     *
     * @return Player
     */
    public function setCompetitor(?bool $competitor): Player
    {
        $this->competitor = $competitor;

        return $this;
    }
}
