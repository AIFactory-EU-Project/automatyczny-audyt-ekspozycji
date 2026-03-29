<?php

namespace App\Entity;

use Doctrine\ORM\Mapping as ORM;

/**
 * @ORM\Entity(repositoryClass="App\Repository\PlanogramElementRepository")
 */
class PlanogramElement
{
    /**
     * @ORM\Id()
     * @ORM\GeneratedValue(strategy="IDENTITY")
     * @ORM\Column(type="integer")
     */
    private $id;

    /**
     * @ORM\ManyToOne(targetEntity="App\Entity\Planogram", inversedBy="planogramElements")
     * @ORM\JoinColumn(name="planogram_id", referencedColumnName="id")
     */
    private $planogram;

    /**
     * @ORM\ManyToOne(targetEntity="App\Entity\Sku", inversedBy="skus")
     * @ORM\JoinColumn(name="sku_id", referencedColumnName="id")
     */
    private $sku;

    /**
     * @ORM\Column(type="integer")
     */
    private $shelf;

    /**
     * @ORM\Column(type="integer")
     */
    private $position;

    /**
     * @ORM\Column(type="integer")
     */
    private $facesCount;

    /**
     * @ORM\Column(type="integer")
     */
    private $stackCount;

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getPlanogram(): ?Planogram
    {
        return $this->planogram;
    }

    public function setPlanogram(Planogram $planogram): self
    {
        $this->planogram = $planogram;

        return $this;
    }

    public function getSku(): ?Sku
    {
        return $this->sku;
    }

    public function setSku(Sku $sku): self
    {
        $this->sku = $sku;

        return $this;
    }

    public function getShelf(): ?int
    {
        return $this->shelf;
    }

    public function setShelf(int $shelf): self
    {
        $this->shelf = $shelf;

        return $this;
    }

    public function getPosition(): ?int
    {
        return $this->position;
    }

    public function setPosition(int $position): self
    {
        $this->position = $position;

        return $this;
    }

    public function getFacesCount(): ?int
    {
        return $this->facesCount;
    }

    public function setFacesCount(int $facesCount): self
    {
        $this->facesCount = $facesCount;

        return $this;
    }

    public function getStackCount(): ?int
    {
        return $this->stackCount;
    }

    public function setStackCount(int $stackCount): self
    {
        $this->stackCount = $stackCount;

        return $this;
    }
}
