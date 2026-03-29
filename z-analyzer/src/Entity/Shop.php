<?php

namespace App\Entity;

use Doctrine\Common\Collections\ArrayCollection;
use Doctrine\Common\Collections\Collection;
use Doctrine\ORM\Mapping as ORM;
use Symfony\Component\Serializer\Annotation\Groups;

/**
 * @ORM\Entity(repositoryClass="App\Repository\ShopRepository")
 */
class Shop
{
    /**
     * @ORM\Id()
     * @ORM\GeneratedValue()
     * @ORM\Column(type="integer")
     * @Groups({"API"})
     */
    private $id;

    /**
     * @ORM\Column(type="string", length=255)
     * @Groups({"API"})
     */
    private $name;

    /**
     * @ORM\Column(type="string", length=255)
     * @Groups({"API"})
     */
    private $code;

    /**
     * @ORM\Column(type="string", length=255, nullable=true)
     * @Groups({"API"})
     */
    private $street;

    /**
     * @ORM\Column(type="string", length=255, nullable=true)
     * @Groups({"API"})
     */
    private $zipCode;

    /**
     * @ORM\Column(type="string", length=255, nullable=true)
     * @Groups({"API"})
     */
    private $city;

    /**
     * @ORM\OneToMany(targetEntity="App\Entity\Camera", mappedBy="shop")
     */
    private $cameras;

    /**
     * @ORM\OneToMany(targetEntity="App\Entity\ShopPlanogramAssignment", mappedBy="shop")
     */
    private $shopPlanogramAssignments;

    public function __construct()
    {
        $this->cameras = new ArrayCollection();
        $this->shopPlanogramAssignments = new ArrayCollection();
    }

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getName(): ?string
    {
        return $this->name;
    }

    public function setName(string $name): self
    {
        $this->name = $name;

        return $this;
    }

    public function getCode(): ?string
    {
        return $this->code;
    }

    public function setCode(string $code): self
    {
        $this->code = $code;

        return $this;
    }

    public function getStreet(): ?string
    {
        return $this->street;
    }

    public function setStreet(?string $street): self
    {
        $this->street = $street;

        return $this;
    }

    public function getZipCode(): ?string
    {
        return $this->zipCode;
    }

    public function setZipCode(?string $zipCode): self
    {
        $this->zipCode = $zipCode;

        return $this;
    }

    public function getCity(): ?string
    {
        return $this->city;
    }

    public function setCity(string $city): self
    {
        $this->city = $city;

        return $this;
    }

    public function getCameras(): Collection
    {
        return $this->cameras;
    }

    public function getShopPlanogramAssignments(): Collection
    {
        return $this->shopPlanogramAssignments;
    }
}
